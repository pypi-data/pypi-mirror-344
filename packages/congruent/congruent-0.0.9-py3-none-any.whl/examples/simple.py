from congruent.schemas.completion import CompletionRequest
from congruent.schemas.message import Message
from examples.utils import get_completion, get_default_model


SYSTEM_PROMPT = """You are a precise multi-label classification system.
Respond in the following JSON format:
{
    "labels": [
        {"name": "label_name", "category": "category_name", "confidence": 0.95}
    ]
}
Ensure confidence scores are between 0 and 1."""


def main(model="openai"):
    # Create a openai request
    request = CompletionRequest(
        messages=[Message(role="user", content="Hello, how are you?")],
        model=get_default_model(model),
        temperature=0.7,
        max_tokens=50,
    )

    # Get completion
    response = get_completion(model, request)
    print("+-+" * 10)
    print(f"Response from {response.provider} ({response.model}): {response.content}")


if __name__ == "__main__":
    print("+-+" * 10)
    print("OpenAI")
    main()
    print("+-+" * 10)
    print("Gemini")
    main(model="gemini")
    print("+-+" * 10)
    print("Anthropic")
    main(model="anthropic")
