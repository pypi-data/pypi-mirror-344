import asyncio

from typing import Iterable, List

from pydantic import BaseModel, Field, ValidationInfo, model_validator

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion


class Tag(BaseModel):
    id: int
    name: str

    @model_validator(mode="after")
    def validate_ids(self, info: ValidationInfo):
        context = info.context
        if context:
            tags: List[Tag] = context.get("tags")
            assert self.id in {tag.id for tag in tags}, (
                f"Tag ID {self.id} not found in context"
            )
            assert self.name in {tag.name for tag in tags}, (
                f"Tag name {self.name} not found in context"
            )
        return self


class TagWithInstructions(Tag):
    instructions: str


class TagRequest(BaseModel):
    texts: List[str]
    tags: List[TagWithInstructions]


class TagResponse(BaseModel):
    texts: List[str]
    predictions: List[Tag]


@model_validator(mode="after")
def validate_ids(self, info: ValidationInfo):
    context = info.context
    if context:
        tags: List[Tag] = context.get("tags")
        assert self.id in {tag.id for tag in tags}, (
            f"Tag ID {self.id} not found in context"
        )
        assert self.name in {tag.name for tag in tags}, (
            f"Tag name {self.name} not found in context"
        )
    return self


async def tag_single_request(
    model: str, text: str, tags: List[Tag]
) -> Tag:
    allowed_tags = [(tag.id, tag.name) for tag in tags]
    allowed_tags_str = ", ".join([f"`{tag}`" for tag in allowed_tags])
    messages = [
        Message(role="system", content="You are a world-class text tagging system."),
        Message(role="user", content=f"Describe the following text: `{text}`"),
        Message(role="user", content=f"Here are the allowed tags: {allowed_tags_str}"),
    ]
    request = CompletionRequest(
        messages=messages,
        model=get_default_model(model),
        response_format=Tag,  # Minimizes the hallucination of tags that are not in the allowed tags.
    )

    return await get_completion(model, request, is_async=True)


async def tag_request(
    model: str, request: TagRequest
) -> TagResponse:
    predictions = await asyncio.gather(
        *[
            tag_single_request(model=model, text=text, tags=request.tags)
            for text in request.texts
        ]
    )
    return TagResponse(
        texts=request.texts,
        predictions=[p.parsed for p in predictions],
    )


tags = [
    TagWithInstructions(id=0, name="personal", instructions="Personal information"),
    TagWithInstructions(id=1, name="phone", instructions="Phone number"),
    TagWithInstructions(id=2, name="email", instructions="Email address"),
    TagWithInstructions(id=3, name="address", instructions="Address"),
    TagWithInstructions(id=4, name="Other", instructions="Other information"),
]

# Texts will be a range of different questions.
# Such as "How much does it cost?", "What is your privacy policy?", etc.
texts = [
    "What is your phone number?",
    "What is your email address?",
    "What is your address?",
    "What is your privacy policy?",
]

# The request will contain the texts and the tags.
request = TagRequest(texts=texts, tags=tags)


# The response will contain the texts, the predicted tags, and the confidence.
async def single_tag(model="openai"):
    response = await tag_request(model=model, request=request)
    print(response.model_dump_json(indent=2))


### impoving the model


class TagWithConfidence(Tag):
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="The confidence of the prediction, 0 is low, 1 is high",
    )


tags = [
    Tag(id=0, name="personal"),
    Tag(id=1, name="phone"),
    Tag(id=2, name="email"),
    Tag(id=3, name="address"),
    Tag(id=4, name="Other"),
]

# Texts will be a range of different questions.
# Such as "How much does it cost?", "What is your privacy policy?", etc.
text = "What is your phone number?"


class Tags(BaseModel):
    tags: Iterable[Tag]


async def get_tags(
    model: str, text: List[str], tags: List[Tag]
) -> List[Tag]:
    allowed_tags = [(tag.id, tag.name) for tag in tags]
    allowed_tags_str = ", ".join([f"`{tag}`" for tag in allowed_tags])
    messages = [
        Message(role="system", content="You are a world-class text tagging system."),
        Message(role="user", content=f"Describe the following text: `{text}`"),
        Message(role="user", content=f"Here are the allowed tags: {allowed_tags_str}"),
    ]

    request = CompletionRequest(
        model=get_default_model(model),
        messages=messages,
        response_format=Tags,
    )
    return await get_completion(
        model=model,
        request=request,
        is_async=True,
    )


async def multi_tags(model="openai"):
    tag_results = await get_tags(
        model=model, text=text, tags=tags
    )
    for tag in tag_results:
        print(tag)
        # > id=1 name='phone'


async def main(model="openai"):
    print("+-+" * 10)
    print(model)
    print("+-+" * 10)
    print("Single Tag")
    await single_tag(model)
    print("+-+" * 10)
    print("Multi Tag")
    await multi_tags(model)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main(model="gemini"))
    asyncio.run(main(model="anthropic"))
