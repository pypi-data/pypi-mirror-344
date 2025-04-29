import os

from typing import Any

import anthropic
import openai

from dotenv import load_dotenv

from congruent.llm.service import LLMService
from congruent.llm.manager import pm
from congruent.schemas.completion import CompletionRequest

load_dotenv()

pm.register_default_providers()
llm_openai = LLMService(client=openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
llm_async_openai = LLMService(
    client=openai.AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
)
llm_gemini = LLMService(
    client=openai.OpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url=os.environ["GEMINI_BASE_URL"])
)
llm_async_gemini = LLMService(
    client=openai.AsyncOpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url=os.environ["GEMINI_BASE_URL"])
)
llm_anthropic = LLMService(
    client=anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
)
llm_async_anthropic = LLMService(
    client=anthropic.AsyncClient(api_key=os.environ["ANTHROPIC_API_KEY"])
)


def get_default_model(mode: str = "openai") -> str:
    """
    Get the default model based on the mode.
    """
    if mode == "openai":
        return "gpt-4o-mini"
    elif mode == "anthropic":
        return "claude-3-5-sonnet-20241022"
    elif mode == "gemini":
        return "gemini-2.0-flash"
    else:
        raise ValueError(f"Unknown mode: {mode}")


def get_completion(model: str, request: CompletionRequest, is_async: bool = False) -> Any:
    """
    Get the completion from the LLM based on the model and prompt.
    """
    if model == "openai":
      return llm_async_openai.get_completion_async(request) if is_async else llm_openai.get_completion(request)
    elif model == "anthropic":
        return llm_async_anthropic.get_completion_async(request) if is_async else llm_anthropic.get_completion(request)
    elif model == "gemini":
        return llm_async_gemini.get_completion_async(request) if is_async else llm_gemini.get_completion(request)
    else:
        raise ValueError(f"Unknown model: {model}")
