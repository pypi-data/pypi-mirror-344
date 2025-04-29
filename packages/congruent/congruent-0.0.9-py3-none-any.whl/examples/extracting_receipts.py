from pydantic import BaseModel, model_validator

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion



class Item(BaseModel):
    name: str
    price: float
    quantity: int


class Receipt(BaseModel):
    items: list[Item]
    total: float

    @model_validator(mode="after")
    def check_total(self):
        items = self.items
        total = self.total
        calculated_total = sum(item.price * item.quantity for item in items)
        if abs(calculated_total - total) > 0.01:
            raise ValueError(
                f"Total {total} does not match the sum of item prices {calculated_total}"
            )
        return self


def extract(url: str, model="openai") -> Receipt:
    messages = [
        Message(
            role="user",
            content=[
                {
                    "type": "image_url",
                    "image_url": {"url": url, "useBase64": model != "openai"},
                },
                {
                    "type": "text",
                    "text": "Analyze the image and return the items in the receipt and the total amount.",
                },
            ],
        )
    ]
    request = CompletionRequest(
        model=get_default_model(model),
        response_format=Receipt,
        messages=messages,
        max_tokens=4000,
    )
    result = get_completion(model, request)
    return result.parsed


url = "https://templates.mediamodifier.com/645124ff36ed2f5227cbf871/supermarket-receipt-template.jpg"


print("+-+" * 10)
print("OpenAI")
print(extract(url))
print("+-+" * 10)
print("Gemini")
print(extract(url, model="gemini"))
print("+-+" * 10)
print("Anthropic")
print(extract(url, model="anthropic"))
print("+-+" * 10)

