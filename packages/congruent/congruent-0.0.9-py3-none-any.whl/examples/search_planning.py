from typing import Literal

from pydantic import BaseModel, Field

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion


class Search(BaseModel):
    query: str = Field(..., description="Query to search for relevant content")
    type: Literal["web", "image", "video"] = Field(..., description="Type of search")

    async def execute(self):
        print(
            f"Searching for `{self.title}` with query `{self.query}` using `{self.type}`"
        )


class SearchPlan(BaseModel):
    searches: list[Search]


def segment(data: str, model="openai") -> SearchPlan:
    messages = [
        Message(
            role="user",
            content=f"Consider the data below: '\n{data}' and segment it into multiple search queries",
        ),
    ]
    request = CompletionRequest(
        model=get_default_model(model),
        response_format=SearchPlan,
        messages=messages,
        max_tokens=1000,
    )
    result = get_completion(model, request)
    print(result.parsed)


if __name__ == "__main__":
    print("+-+" * 10)
    print("OpenAI")
    segment("Search for a picture of a cat and a video of a dog")
    print("+-+" * 10)
    print("Gemini")
    segment("Search for a picture of a cat and a video of a dog", model="gemini")
    print("+-+" * 10)
    print("Anthropic")
    segment("Search for a picture of a cat and a video of a dog", model="anthropic")
# > {"query":"picture of a cat","type":"image"}
# > {"query":"video of a dog","type":"video"}
