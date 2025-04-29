from pydantic import BaseModel, Field

from congruent.schemas.completion import CompletionRequest
from congruent.schemas.message import Message

from examples.utils import get_default_model, get_completion


class AnonymizationResult(BaseModel):
    original: str
    anonymized: str
    replacements: str = Field(
        description="The replacements made during anonymization: ({original} -> {placeholder})",
    )


def anonymize_text(text: str, model="openai") -> AnonymizationResult:
    messages = [
        Message(
            role="system",
            content="You are an expert at anonymizing text by replacing personal information with generic placeholders.",
        ),
        Message(role="user", content=f"Anonymize the following text: {text}"),
    ]
    request = CompletionRequest(
        model=get_default_model(model),
        response_format=AnonymizationResult,
        messages=messages,
    )
    return get_completion(model, request)


if __name__ == "__main__":
    original_text = "John Doe, born on 05/15/1980, lives at 123 Main St, New York. His email is john.doe@example.com."

    print("+-+" * 10)
    print("OpenAI")
    print("+-+" * 10)
    result = anonymize_text(original_text)
    print(f"Prased: {result.parsed}")
    print(f"Original: {result.parsed.original}")
    print(f"Anonymized: {result.parsed.anonymized}")
    print(f"Replacements: {result.parsed.replacements}")

    print("+-+" * 10)
    print("Gemini")
    print("+-+" * 10)
    result = anonymize_text(original_text, model="gemini")
    print(f"Prased: {result.parsed}")
    print(f"Original: {result.parsed.original}")
    print(f"Anonymized: {result.parsed.anonymized}")
    print(f"Replacements: {result.parsed.replacements}")

    print("+-+" * 10)
    print("Anthropic")
    print("+-+" * 10)
    result = anonymize_text(original_text, model="anthropic")
    print(f"Prased: {result.parsed}")
    print(f"Original: {result.parsed.original}")
    print(f"Anonymized: {result.parsed.anonymized}")
    print(f"Replacements: {result.parsed.replacements}")
