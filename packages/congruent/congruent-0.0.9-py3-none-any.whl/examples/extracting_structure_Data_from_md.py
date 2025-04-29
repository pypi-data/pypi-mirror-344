import json
import pandas as pd

from io import StringIO
from textwrap import dedent
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    BeforeValidator,
    InstanceOf,
    PlainSerializer,
    WithJsonSchema,
)

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion

def md_to_df(data: Any) -> Any:
    # Convert markdown to DataFrame
    if isinstance(data, str):
        return (
            pd.read_csv(
                StringIO(data),  # Process data
                sep="|",
                index_col=1,
            )
            .dropna(axis=1, how="all")
            .iloc[1:]
            .applymap(lambda x: x.strip())
        )
    return data


MarkdownDataFrame = Annotated[
    InstanceOf[pd.DataFrame],
    BeforeValidator(md_to_df),
    PlainSerializer(lambda df: df.to_markdown()),
    WithJsonSchema(
        {
            "type": "string",
            "description": "The markdown representation of the table, each one should be tidy, do not try to join tables that should be seperate",
        }
    ),
]


class Table(BaseModel):
    caption: str
    dataframe: MarkdownDataFrame


def main(model: str = "openai"):

    url = "https://a.storyblok.com/f/47007/2400x2000/bf383abc3c/231031_uk-ireland-in-three-charts_table_v01_b.png"

    system_message = dedent(
        f"""
        As a genius expert, your task is to understand the content and provide
        the parsed objects in json that match the following json_schema:\n

        {json.dumps(Table.model_json_schema(), indent=2, ensure_ascii=False)}

        Make sure to return an instance of the JSON, not the schema itself
        """
    )
    messages = [
        Message(
            role="system",
            content=system_message,
        ),
        Message(
            role="user",
            content=[
                {"type": "text", "text": "Extract table from image."},
                {"type": "image_url", "image_url": {"url": url, "useBase64": model != "openai"}},
                {
                    "type": "text",
                    "text": "Return the correct JSON response within a ```json codeblock. not the JSON_SCHEMA",
                },
            ],
        ),
    ]

    # OpenAI
    request = CompletionRequest(
        messages=messages,
        model=get_default_model(model),
        response_format=Table,
        max_tokens=1800,
    )
    response = get_completion(model, request)

    data = response.parsed

    print(data.caption)
    print(" " * 10)
    print(data.dataframe)

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
