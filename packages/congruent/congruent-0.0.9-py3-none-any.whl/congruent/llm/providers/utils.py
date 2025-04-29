import os
import base64
import typing
import inspect

from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Callable, Optional, Union, List

from clipped.compact.pydantic import Field, create_model
from docstring_parser import parse


def is_simple_type(
    response_model: typing.Union[type[BaseModel], str, int, float, bool, typing.Any],
) -> bool:
    try:
        if inspect.isclass(response_model) and issubclass(response_model, BaseModel):
            return False
    except TypeError:
        return False

    # Get the origin of the response model
    origin = typing.get_origin(response_model)

    # Handle Python 3.10 special case for list[int | str] type patterns
    # In Python 3.10, list[int | str] has an origin of typing.Iterable
    # but we still want to treat it as a simple type
    if origin in {typing.Iterable, typing.Iterator}:
        # Check if it's a list with Union type arguments (like list[int | str])
        args = typing.get_args(response_model)
        if args and len(args) == 1 and typing.get_origin(args[0]) is typing.Union:
            # This is a list with a Union type, which should be treated as a simple type
            return True
        # Otherwise, it's a streaming type
        return False

    if response_model in {
        str,
        int,
        float,
        bool,
    }:
        return True

    # If the response_model is a simple type like annotated
    if origin in {
        typing.Annotated,
        typing.Literal,
        typing.Union,
        list,  # origin of List[T] is list
        tuple,  # origin of Tuple[T] is tuple
    }:
        return True

    if inspect.isclass(response_model) and issubclass(response_model, Enum):
        return True

    return False


def _recursive_set_additional_properties_false(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """Recursively set additionalProperties to False in a JSON Schema."""
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            schema["additionalProperties"] = False

        # Recursively check all possible nested schema containers
        for key in ("properties", "definitions", "$defs"):
            if key in schema:
                for value in schema[key].values():
                    _recursive_set_additional_properties_false(value)
        if "items" in schema:
            _recursive_set_additional_properties_false(schema["items"])
        for key in ("allOf", "anyOf", "oneOf"):
            if key in schema:
                for subschema in schema[key]:
                    _recursive_set_additional_properties_false(subschema)
    return schema


def _remove_defaults(schema):
    if isinstance(schema, dict):
        # Remove 'default' key at this level
        schema = {k: _remove_defaults(v) for k, v in schema.items() if k != "default"}
    elif isinstance(schema, list):
        schema = [_remove_defaults(item) for item in schema]
    return schema


def convert_to_openai_function(
    obj: Union[dict[str, Any], type, Callable],
    *,
    strict: Optional[bool] = None,
) -> dict[str, Any]:
    """Convert a raw function/class/dict to an OpenAI function schema.

    This function handles multiple input formats and converts them to the OpenAI function schema format
    used for function calling. The following input formats are supported:

    - Dictionary in OpenAI function format (with name, description, parameters)
    - Dictionary in JSON Schema format (with title, description, properties)
    - Dictionary in Anthropic tool format (with name, description, input_schema)
    - Dictionary in Amazon Bedrock Converse format (with toolSpec)
    - Pydantic BaseModel class
    - Python function/callable

    Args:
        obj: The object to convert. Can be a dictionary in one of the supported formats,
            a Pydantic BaseModel class, or a Python callable.
        strict: If True, enforces strict JSON Schema validation on model output.
            If None, the strict validation flag is omitted from the schema.

    Returns:
        dict: A dictionary in OpenAI function schema format containing:
            - name: The function name
            - description: The function description
            - parameters: The JSON Schema for the function parameters

    Raises:
        ValueError: If the input object format is not supported or cannot be converted.
    """

    obj_schema = None
    # simple type
    if is_simple_type(obj):
        # Convert simple types to a Pydantic model
        function_model = simple_type_to_pydantic(obj)
        obj_schema = convert_pydantic_to_schema(function_model)
    # already in OpenAI function format
    if isinstance(obj, dict) and all(
        k in obj for k in ("name", "description", "parameters")
    ):
        obj_schema = obj
    # a JSON schema with title and description
    if (
        not obj_schema
        and isinstance(obj, dict)
        and all(k in obj for k in ("title", "description", "properties"))
    ):
        obj = obj.copy()
        obj_schema = {
            "name": obj.pop("title"),
            "description": obj.pop("description"),
            "parameters": obj,
        }
    # an Anthropic format tool
    if (
        not obj_schema
        and isinstance(obj, dict)
        and all(k in obj for k in ("name", "description", "input_schema"))
    ):
        obj_schema = {
            "name": obj["name"],
            "description": obj["description"],
            "parameters": obj["input_schema"],
        }
    # an Amazon Bedrock Converse format tool
    if not obj_schema and isinstance(obj, dict) and "toolSpec" in obj:
        obj_schema = {
            "name": obj["toolSpec"]["name"],
            "description": obj["toolSpec"]["description"],
            "parameters": obj["toolSpec"]["inputSchema"]["json"],
        }
    # a Pydantic BaseModel
    if not obj_schema and isinstance(obj, type):
        obj_schema = convert_pydantic_to_schema(obj)
    if not obj_schema and callable(obj):
        # Create a schema from the function signature
        function_model = function_to_pydantic_model(obj)
        obj_schema = convert_pydantic_to_schema(function_model)
    if not obj_schema:
        msg = (
            f"Unsupported function\n\n{obj}\n\nFunctions must be passed in"
            " as Dict, pydantic.BaseModel, or Callable. If they're a dict they must"
            " either be in OpenAI function format or valid JSON schema with top-level"
            " 'title' and 'description' keys."
        )
        raise ValueError(msg)

    def _ensure_strict_json_schema(json_schema: dict, path=(), root=None) -> dict:
        """Recursively ensure 'required' includes all property keys and properties are strict."""
        if root is None:
            root = json_schema
        if isinstance(json_schema, dict):
            if json_schema.get("type") == "object":
                properties = json_schema.get("properties")
                if isinstance(properties, dict):
                    # Ensure 'required' includes all property keys
                    json_schema["required"] = list(properties.keys())
                    # Recurse into each property
                    json_schema["properties"] = {
                        key: _ensure_strict_json_schema(
                            prop_schema, path=(*path, "properties", key), root=root
                        )
                        for key, prop_schema in properties.items()
                    }
            # Recurse into items, $defs, allOf, anyOf, oneOf
            if "items" in json_schema:
                json_schema["items"] = _ensure_strict_json_schema(
                    json_schema["items"], path=(*path, "items"), root=root
                )
            for key in ("$defs", "definitions"):
                if key in json_schema:
                    for k, v in json_schema[key].items():
                        json_schema[key][k] = _ensure_strict_json_schema(
                            v, path=(*path, key, k), root=root
                        )
            for key in ("allOf", "anyOf", "oneOf"):
                if key in json_schema:
                    json_schema[key] = [
                        _ensure_strict_json_schema(sub, path=(*path, key, i), root=root)
                        for i, sub in enumerate(json_schema[key])
                    ]
        return json_schema

    if strict is not None:
        obj_schema["strict"] = strict
        if strict:
            # As of 08/06/24, OpenAI requires that additionalProperties be supplied and
            # set to False if strict is True.
            # All properties layer needs 'additionalProperties=False'
            obj_schema["parameters"] = _recursive_set_additional_properties_false(
                obj_schema["parameters"]
            )
            # Ensure 'required' is correct everywhere
            obj_schema["parameters"] = _ensure_strict_json_schema(
                obj_schema["parameters"]
            )
            # Remove all 'default' keys from the schema
            obj_schema["parameters"] = _remove_defaults(obj_schema["parameters"])
    return obj_schema


def convert_pydantic_to_schema(
    pydantic_model: type,
) -> dict[str, Any]:
    """Convert a Pydantic BaseModel to a JSON Schema.

    This function extracts the JSON Schema from a Pydantic BaseModel using the appropriate method
    based on the Pydantic version.

    Args:
        pydantic_model: The Pydantic BaseModel to convert.

    Returns:
        dict: A dictionary representing the JSON Schema.
    """
    if hasattr(pydantic_model, "model_json_schema"):
        schema = pydantic_model.model_json_schema()  # Pydantic 2
    elif hasattr(pydantic_model, "schema"):
        schema = pydantic_model.schema()  # Pydantic 1
    else:
        return {}

    # Inline any nested models from $defs
    if "$defs" in schema:

        def resolve_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj and obj["$ref"].startswith("#/$defs/"):
                    ref_name = obj["$ref"].split("/")[-1]
                    resolved = schema["$defs"][ref_name].copy()
                    # Preserve any existing keys from the ref object (like description)
                    resolved.update({k: v for k, v in obj.items() if k != "$ref"})
                    return resolved
                return {k: resolve_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [resolve_refs(item) for item in obj]
            return obj

        schema = resolve_refs(schema)

    docstring = parse(pydantic_model.__doc__ or "")
    parameters = {k: v for k, v in schema.items() if k not in ("title", "description")}
    for param in docstring.params:
        if (param_name := param.arg_name) in parameters["properties"] and (
            param_description := param.description
        ):
            if "description" not in parameters["properties"][param_name]:
                parameters["properties"][param_name]["description"] = param_description

    parameters["required"] = sorted(
        k for k, v in parameters["properties"].items() if "default" not in v
    )

    return {
        "name": schema.get("title", pydantic_model.__name__),
        "description": schema.get("description", docstring.short_description or ""),
        "parameters": parameters,
    }


def function_to_pydantic_model(func):
    """Convert a Python function to a Pydantic BaseModel.

    This function extracts the parameters from a Python function's signature and creates a Pydantic BaseModel
    with fields corresponding to the function's parameters.

    Args:
        func: The Python function to convert.

    Returns:
        Pydantic BaseModel: A Pydantic BaseModel with fields corresponding to the function's parameters.
    """
    # Parse the function signature
    signature = inspect.signature(func)

    # Extract docstring info
    docstring_params = {}
    if func.__doc__:
        doc = parse(func.__doc__)
        docstring_params = {param.arg_name: param.description for param in doc.params}

    # Create field definitions
    fields = {}
    for name, param in signature.parameters.items():
        field_type = param.annotation
        description = docstring_params.get(name, f"Parameter: {name}")

        # Handle Optional types
        default = ... if param.default == param.empty else param.default
        if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
            # Check if it's Optional (Union with NoneType)
            types = field_type.__args__
            if type(None) in types:
                # Get the actual type (excluding NoneType)
                field_type = next(t for t in types if t != type(None))
                default = None if param.default == param.empty else param.default

        fields[name] = (field_type, Field(default=default, description=description))

    # Create dynamic model
    model_name = f"{func.__name__.title()}Model"
    return create_model(model_name, **fields)


def simple_type_to_pydantic(
    simple_type: Any,
) -> type:
    fields = {
        "value": (simple_type, Field()),
    }

    return create_model("SimpleTypeModel", **fields)


def convert_to_base64(url: str, allowed_media_types: List = None) -> tuple[str, str]:
    # Convert URL images to base64
    import requests

    response = requests.get(url)
    media_type = response.headers.get("Content-Type", "application/octet-stream")
    # Infer media type from file extension if Content-Type is application/octet-stream
    if media_type == "application/octet-stream":
        ext = os.path.splitext(url)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            media_type = "image/jpeg"
        elif ext == ".png":
            media_type = "image/png"
        elif ext == ".gif":
            media_type = "image/gif"
        elif ext == ".webp":
            media_type = "image/webp"
    else:
        for _type in allowed_media_types:
            if _type in media_type:
                media_type = _type
    if allowed_media_types and media_type not in allowed_media_types:
        raise ValueError(f"Unsupported image media type: {media_type}")
    return base64.b64encode(response.content).decode(), media_type


async def async_convert_to_base64(
    url: str, allowed_media_types: list = None
) -> tuple[str, str]:
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        media_type = response.headers.get("Content-Type", "application/octet-stream")
        if media_type == "application/octet-stream":
            ext = os.path.splitext(url)[1].lower()
            if ext in [".jpg", ".jpeg"]:
                media_type = "image/jpeg"
            elif ext == ".png":
                media_type = "image/png"
            elif ext == ".gif":
                media_type = "image/gif"
            elif ext == ".webp":
                media_type = "image/webp"
        if allowed_media_types and media_type not in allowed_media_types:
            raise ValueError(f"Unsupported image media type: {media_type}")
        return base64.b64encode(response.content).decode(), media_type


def get_base64_from_url(
    url: str, allowed_media_types: List = None, is_async: bool = False
) -> tuple[str, str]:
    if url.startswith("data:"):
        # Handle base64 images
        media_type = url.split(";")[0].split(":")[1]
        if media_type not in allowed_media_types:
            raise ValueError(f"Unsupported image media type: {media_type}")
        return url.split(",")[1], media_type

    if is_async:
        return async_convert_to_base64(url, allowed_media_types)
    return convert_to_base64(url, allowed_media_types)
