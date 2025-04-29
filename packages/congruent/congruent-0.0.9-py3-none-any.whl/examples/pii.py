from typing import List
from pydantic import BaseModel

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion


# Define Schemas for PII data
class Data(BaseModel):
    index: int
    data_type: str
    pii_value: str


class PIIDataExtraction(BaseModel):
    """
    Extracted PII data from a document, all data_types should try to have consistent property names
    """

    private_data: List[Data]

    def scrub_data(self, content: str) -> str:
        """
        Iterates over the private data and replaces the value with a placeholder in the form of
        <{data_type}_{i}>
        """
        for i, data in enumerate(self.private_data):
            content = content.replace(data.pii_value, f"<{data.data_type}_{i}>")
        return content


EXAMPLE_DOCUMENT = """
John Doe is a person living at 123 Main St, Anytown, USA.
You can contact him at john.doe@example.com or call (555) 123-4567.
His Social Security Number is 123-45-6789.
"""

def main(model="openai"):
    request = CompletionRequest(
        model=get_default_model(model),
        response_format=PIIDataExtraction,
        messages=[
            Message(
                role="system",
                content="You are a world class PII scrubbing model, Extract the PII data from the following document",
            ),
            Message(
                role="user",
                content=EXAMPLE_DOCUMENT,
            ),
        ],
    )  # type: ignore

    result = get_completion(model, request)

    print("Extracted PII Data:")
    # > Extracted PII Data:
    print(result.parsed)


"""
{"private_data":[{"index":0,"data_type":"Name","pii_value":"John Doe"},{"index":1,"data_type":"Email","pii_value":"john.doe@example.com"},{"index":2,"data_type":"Phone Number","pii_value":"(555) 123-4567"},{"index":3,"data_type":"Address","pii_value":"123 Main St, Anytown, USA"},{"index":4,"data_type":"Social Security Number","pii_value":"123-45-6789"}]}
"""
if __name__ == "__main__":
    print("+-+" * 10)
    print("OpenAI")
    main(model="openai")
    print("+-+" * 10)
    print("Gemini")
    main(model="gemini")
    print("+-+" * 10)
    print("Anthropic")
    main(model="anthropic")

