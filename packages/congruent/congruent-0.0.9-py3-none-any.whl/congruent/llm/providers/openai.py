from typing import Any, Dict, List, Literal, Optional, T, Union

from openai import NOT_GIVEN
from openai.types.chat import ChatCompletionMessageToolCall

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
    obj: type[T],
    strict: Optional[bool] = None,
) -> Dict:
    obj_schema = convert_to_openai_function(obj, strict=strict)
    return {
        "type": "function",
        "function": obj_schema,
    }


def _prepare_tools(
    tools: Optional[List[Dict[str, Any]]], strict: Optional[bool] = None
) -> List[Dict[str, Any]]:
    if tools is None:
        return NOT_GIVEN
    return [_prepare_tool(tool, strict) for tool in tools]


def _prepare_parallel_tool_calls(
    parallel_tool_calls: Optional[bool],
    tools_count: int,
) -> Optional[bool]:
    if parallel_tool_calls is None or tools_count == 0:
        return NOT_GIVEN
    return parallel_tool_calls


def _prepare_tool_choice(
    tool_choice: Optional[Union[Literal["none", "required", "auto"], str]],
) -> Optional[Dict[str, Any]]:
    if tool_choice is None:
        return NOT_GIVEN
    elif tool_choice in {"auto", "required", "none"}:
        return tool_choice
    else:
        return {
            "type": "function",
            "function": {
                "name": tool_choice,
            },
        }


def _prepare_response_format(
    response_format: Optional[Dict[str, Any]],
    strict: Optional[bool] = None,
) -> Dict[str, Any]:
    if response_format is None:
        return NOT_GIVEN
    model_schema = convert_to_openai_function(response_format, strict=strict)
    return {
        "type": "json_schema",
        "json_schema": {
            "name": model_schema["name"],
            "schema": model_schema["parameters"],
            "strict": strict,
        },
    }


def _format_message_content(
    content: Union[Dict[str, Any], str], is_async: bool
) -> Dict[str, Any]:
    """Format attachment for OpenAI API"""
    if not isinstance(content, dict):
        return {"type": "text", "text": str(content)}

    # Handle image attachments
    if content.get("type") == "image_url":
        if not content["image_url"].get("useBase64"):
            return content
        # handle as base64
        url = content["image_url"]["url"]
        allowed_media_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        data, media_type = get_base64_from_url(url, allowed_media_types, is_async)
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{media_type};base64,{data}"},
        }

    # Handle audio attachments
    elif content.get("type") == "input_audio":
        audio_data = content["input_audio"]
        return {
            "type": "input_audio",
            "input_audio": {
                "data": audio_data["data"],
                "format": audio_data.get("format", "mp3"),
            },
        }

    return content


def _prepare_messages(
    request: CompletionRequest, is_async: bool
) -> List[Dict[str, Any]]:
    messages = []
    for msg in request.messages:
        if isinstance(msg.content, str):
            messages.append({"role": msg.role, "content": msg.content})
        else:
            messages.append(
                {
                    "role": msg.role,
                    "content": [
                        _format_message_content(item, is_async) for item in msg.content
                    ],
                }
            )
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

    return function_model.model_validate_json(tool_response)


def _parse_tools(tool_calls, request: CompletionRequest) -> List[Any]:
    if tool_calls is None:
        return []
    tool_schemas_by_name = request.tools_by_name()
    parsed_tools = []
    for tool_call in tool_calls:
        if isinstance(tool_call, ChatCompletionMessageToolCall):
            tool_name = tool_call.function.name
            tool_response = tool_call.function.arguments
        else:
            tool_name = tool_call[0]
            tool_response = tool_call[1]
        if tool_name in tool_schemas_by_name:
            tool_schema = tool_schemas_by_name[tool_name]
            parsed_tool = _parse_tool(tool_schema, tool_response)
            parsed_tools.append(parsed_tool)
        else:
            parsed_tools.append(tool_response)
    return parsed_tools


def _parse_response_format(message, request: CompletionRequest) -> Optional[Any]:
    if not request.response_format or not message.content:
        return None

    return _parse_tool(request.response_format, message.content)


def _prepare_response(request: CompletionRequest, response: Any) -> CompletionResponse:
    tool_calls = None
    if request.tools:
        tool_calls = _parse_tools(response.choices[0].message.tool_calls, request)
    content = response.choices[0].message.content
    parsed = (
        _parse_response_format(response.choices[0].message, request)
        if request.response_format
        else None
    )
    return CompletionResponse(
        content=content,
        parsed=parsed,
        tool_calls=tool_calls,
        model=request.model,
        provider="openai",
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        raw_response=response.model_dump(),
    )


def _completion(client, request: CompletionRequest) -> CompletionResponse:
    is_async = client.__class__.__name__ == "AsyncOpenAI"
    messages = _prepare_messages(request, is_async)
    tools = _prepare_tools(request.tools, strict=request.strict_schema)
    tool_choice = _prepare_tool_choice(request.tool_choice)
    response_format = _prepare_response_format(
        request.response_format, strict=request.strict_schema
    )
    return client.chat.completions.create(
        model=request.model,
        messages=messages,
        response_format=response_format,
        tools=tools,
        tool_choice=tool_choice,
        parallel_tool_calls=_prepare_parallel_tool_calls(
            request.parallel_tool_calls, len(request.tools or [])
        ),
        temperature=_non_null_or_not_given(request.temperature),
        max_tokens=_non_null_or_not_given(request.max_tokens),
        stop=_non_null_or_not_given(request.stop),
        top_p=_non_null_or_not_given(request.top_p),
        frequency_penalty=_non_null_or_not_given(request.frequency_penalty),
        presence_penalty=_non_null_or_not_given(request.presence_penalty),
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
def validate_client(client) -> Optional[Literal["openai"]]:
    if client.__class__.__name__ in {
        "OpenAI",
        "AsyncOpenAI",
    }:
        return "openai"


@hookimpl
def handle_function(
    obj: type[T],
) -> Dict:
    return _handle_tools(obj)
