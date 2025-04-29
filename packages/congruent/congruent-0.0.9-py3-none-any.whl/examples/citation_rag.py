import re

from typing import List

from pydantic import BaseModel, Field, ValidationInfo, model_validator

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion



class Fact(BaseModel):
    fact: str = Field(...)
    substring_quote: List[str] = Field(...)

    # @model_validator(mode="after")
    # def validate_sources(self, info: ValidationInfo) -> "Fact":
    #     text_chunks = info.context.get("text_chunk", None)
    #     spans = list(self.get_spans(text_chunks))
    #     self.substring_quote = [text_chunks[span[0] : span[1]] for span in spans]
    #     return self

    def get_spans(self, context):
        for quote in self.substring_quote:
            yield from self._get_span(quote, context)

    def _get_span(self, quote, context):
        for match in re.finditer(re.escape(quote), context):
            yield match.span()


class QuestionAnswer(BaseModel):
    question: str = Field(...)
    answer: List[Fact] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self) -> "QuestionAnswer":
        self.answer = [fact for fact in self.answer if len(fact.substring_quote) > 0]
        return self



def main(model="openai"):
    question = "What did the author do during college?"
    context = """
    My name is Jason Liu, and I grew up in Toronto Canada but I was born in China.
    I went to an arts high school but in university I studied Computational Mathematics and physics.
    As part of coop I worked at many companies including Stitchfix, Facebook.
    I also started the Data Science club at the University of Waterloo and I was the president of the club for 2 years.
    """

    messages = [
        Message(
            role="system",
            content="You are a world class algorithm to answer questions with correct and exact citations.",
        ),
        Message(role="user", content=f"{context}"),
        Message(role="user", content=f"Question: {question}"),
    ]

    request = CompletionRequest(
        messages=messages,
        model=get_default_model(model),
        tools=[QuestionAnswer],
    )

    response = get_completion(model, request)
    print(f"Model: {model}")
    print("+-+" * 10)
    print(response.tool_calls)


if __name__ == "__main__":
    main()
    print("+" * 20)
    main(model="gemini")
    print("+" * 20)
    main(model="anthropic")
