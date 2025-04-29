from typing import Any, Dict, List, Literal, Optional, T, Type, Union, Tuple

from anthropic import NOT_GIVEN

from congruent.llm.hookspecs import hookimpl
from congruent.llm.providers.utils import (
    convert_to_openai_function,
    simple_type_to_pydantic,
    function_to_pydantic_model,
    is_simple_type,
    get_base64_from_url,
)
from congruent.schemas.completion import CompletionRequest, CompletionResponse


def _non_null_or_not_given(value: Any) -> Any:
    return value if value is not None else NOT_GIVEN


def _prepare_tool(
    obj: Type[T],
    strict: Optional[bool] = None,
) -> Dict:
    """Convert tools to Anthropic's format"""
    openai_schema = convert_to_openai_function(obj, strict=strict)
    # Convert from OpenAI format to Anthropic format
    return {
        "name": openai_schema["name"],
        "description": openai_schema["description"],
        "input_schema": openai_schema["parameters"],
    }


def _prepare_tools(
    tools: Optional[List[Dict[str, Any]]], strict: Optional[bool] = None
) -> List[Dict[str, Any]]:
    if tools is None:
        return NOT_GIVEN
    return [_prepare_tool(tool, strict) for tool in tools]


def _prepare_tool_choice(
    tool_choice: Optional[Union[Literal["none", "required", "auto"], str]],
    parallel_tool_calls: Optional[bool],
    tools_count: int,
) -> Optional[Dict[str, Any]]:
    if tool_choice is None or tools_count == 0:
        return NOT_GIVEN

    kwargs = {}
    if parallel_tool_calls is not None:
        kwargs = {"disable_parallel_tool_use": not parallel_tool_calls}
    if tool_choice == "auto":
        kwargs["type"] = "auto"
    elif tool_choice == "required":
        kwargs["type"] = "any"
    elif tool_choice == "none":
        kwargs["disable_parallel_tool_use"] = True
    else:
        kwargs["type"] = "tool"
        kwargs["name"] = tool_choice
    return kwargs


def _prepare_response_format(
    tools: Optional[List[Dict[str, Any]]],
    response_format: Optional[Any],
    strict_schema: Optional[bool],
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    if response_format is None:
        return tools, None

    tool = _prepare_tool(response_format, strict=strict_schema)
    # get tool name
    tool_name = tool["name"]
    # check if tool name is in tools
    if not tools:
        tools = [tool]
    else:
        # check if tool name is in tools
        if not any(t["name"] == tool_name for t in tools):
            tools.append(tool)

    return tools, tool_name


def _format_message_content(
    content: Union[Dict[str, Any], str], is_async: bool
) -> Dict[str, Any]:
    """Format attachment for Anthropic API"""
    if not isinstance(content, dict):
        return {"type": "text", "text": str(content)}

    # Handle image attachments
    if content.get("type") == "image_url":
        url = content["image_url"]["url"]
        allowed_media_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        data, media_type = get_base64_from_url(url, allowed_media_types, is_async)
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": data},
        }

    # Handle audio attachments - Anthropic doesn't support audio yet
    elif content.get("type") == "input_audio":
        raise NotImplementedError("Audio attachments are not supported by Anthropic")

    return content


def _validate_role(role: str) -> str:
    if role == "system":
        return "assistant"
    return role


def _prepare_messages(
    request: CompletionRequest, is_async: bool
) -> List[Dict[str, Any]]:
    # Convert messages to Anthropic format, handling attachments
    messages = []
    for msg in request.messages:
        if isinstance(msg.content, str):
            messages.append({"role": _validate_role(msg.role), "content": msg.content})
        else:
            # Format each content item
            content = [_format_message_content(item, is_async) for item in msg.content]
            messages.append({"role": _validate_role(msg.role), "content": content})
    return messages


def _parse_tool(tool_schema, tool_response: Any) -> Optional[Any]:
    if is_simple_type(tool_schema):
        function_model = simple_type_to_pydantic(tool_schema)
    elif isinstance(tool_schema, type):
        function_model = tool_schema
    elif callable(tool_schema):
        function_model = function_to_pydantic_model(tool_schema)
    else:
        return tool_response

    return function_model.model_validate(tool_response)


def _parse_tools(tool_calls, request: CompletionRequest) -> List[Any]:
    if tool_calls is None:
        return []
    tool_schemas_by_name = request.tools_by_name()
    parsed_tools = []
    for tool_call in tool_calls:
        tool_name = tool_call.name
        tool_response = tool_call.input
        if tool_name in tool_schemas_by_name:
            tool_schema = tool_schemas_by_name[tool_name]
            parsed_tool = _parse_tool(tool_schema, tool_response)
            parsed_tools.append(parsed_tool)
        else:
            parsed_tools.append(tool_response)
    return parsed_tools


def _parse_response_format(
    response_format: Optional[Any],
    tool_calls: List[Any],
) -> Optional[Any]:
    if response_format is None:
        return None

    for tool_call in tool_calls:
        tool_name = tool_call.name
        tool_response = tool_call.input
        if tool_name == response_format.__name__:
            return _parse_tool(response_format, tool_response)


def _prepare_response(request: CompletionRequest, response: Any) -> CompletionResponse:
    content = next((c.text for c in response.content if c.type == "text"), None)
    tool_calls = [c for c in response.content if c.type == "tool_use"]
    parsed = None
    if tool_calls and request.tools:
        tool_calls = _parse_tools(tool_calls, request)
    if tool_calls and request.response_format:
        parsed = _parse_response_format(request.response_format, tool_calls)

    return CompletionResponse(
        content=content,
        parsed=parsed,
        tool_calls=tool_calls,
        model=request.model,
        provider="anthropic",
        usage={
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        },
        raw_response=response.model_dump(),
    )


def _completion(client, request: CompletionRequest) -> CompletionResponse:
    is_async = client.__class__.__name__ == "AsyncAnthropic"
    messages = _prepare_messages(request, is_async)
    tools = _prepare_tools(request.tools, strict=request.strict_schema)
    tools, tool_choice = _prepare_response_format(
        tools=tools,
        response_format=request.response_format,
        strict_schema=request.strict_schema,
    )
    tool_choice = _prepare_tool_choice(
        tool_choice or request.tool_choice,
        request.parallel_tool_calls,
        len(request.tools or []),
    )
    return client.messages.create(
        model=request.model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
        temperature=_non_null_or_not_given(request.temperature),
        max_tokens=request.max_tokens or 1024,
        stop_sequences=_non_null_or_not_given(request.stop),
        top_p=_non_null_or_not_given(request.top_p),
    )


@hookimpl
def get_completion(client, request: CompletionRequest) -> CompletionResponse:
    response = _completion(client, request)
    return _prepare_response(request, response)


@hookimpl
async def get_completion_async(
    client, request: CompletionRequest
) -> CompletionResponse:
    response = await _completion(client, request)
    return _prepare_response(request, response)


@hookimpl
def validate_client(client) -> Optional[Literal["anthropic"]]:
    if client.__class__.__name__ in {
        "Anthropic",
        "AsyncAnthropic",
    }:
        return "anthropic"
