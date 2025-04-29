from pydantic import BaseModel, Field

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion

tagging_prompt = """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""


class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


def main(model="openai"):

    content = tagging_prompt.format(
        input="Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
    )
    messages = [Message(role="user", content=content)]

    request = CompletionRequest(
        messages=messages,
        tools=[Classification],
        model=get_default_model(model),
        temperature=0.7,
        max_tokens=500,
    )

    response = get_completion(model, request)

    print("+-+" * 10)
    print(
        f"Response from {response.provider} ({response.model}): {response.tool_calls}"
    )
    print("+-+" * 10)


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
