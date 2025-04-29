from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from congruent.schemas.message import Message


class CompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    mode: Optional[Literal["tools", "json"]] = Field(default="tools")
    tools: Optional[List[Any]] = None
    tool_choice: Optional[Union[Literal["none", "required", "auto"], str]] = None
    parallel_tool_calls: Optional[bool] = None
    response_format: Optional[Any] = None
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    stop: Optional[List[str]] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    strict_schema: Optional[bool] = True

    def tools_by_name(self) -> Dict[str, Any]:
        if self.tools is None:
            return {}
        return {tool.__name__: tool for tool in self.tools}


class CompletionResponse(BaseModel):
    content: Optional[Union[str, Any]] = None
    tool_calls: Optional[List[Any]] = None
    parsed: Optional[Any] = None
    model: str
    provider: str
    usage: Dict[str, int]
    raw_response: Dict[str, Any]
