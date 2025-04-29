import asyncio

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion

SYSTEM_PROMPT = """You are a precise multi-label classification system.
Respond in the following JSON format:
{
    "labels": [
        {"name": "label_name", "category": "category_name", "confidence": 0.95}
    ]
}
Ensure confidence scores are between 0 and 1."""



async def main_async(model: str = "openai"):
    print("Running async main")
    # Initialize the interface

    # Create an OpenAI request
    request = CompletionRequest(
        messages=[Message(role="user", content="Hello, how are you?")],
        model=get_default_model(model),
        temperature=0.7,
        max_tokens=50,
    )

    # Get completion
    response = await get_completion(model, request, is_async=True)
    print("+-+" * 10)
    print(f"Model: {model}")
    print("+-+" * 10)
    print(f"Response from {response.provider} ({response.model}): {response.content}")
    print("+-+" * 10)



if __name__ == "__main__":
    asyncio.run(main_async())
    asyncio.run(main_async("anthropic"))
    asyncio.run(main_async("gemini"))
