from typing import List, Literal

from pydantic import BaseModel, Field
from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion


class Query(BaseModel):
    """Class representing a single question in a query plan."""

    id: int = Field(..., description="Unique id of the query")
    question: str = Field(
        ...,
        description="Question asked using a question answering system",
    )
    dependencies: List[int] = Field(
        default_factory=list,
        description="List of sub questions that need to be answered before asking this question",
    )
    node_type: Literal["SINGLE", "MERGE_MULTIPLE_RESPONSES"] = Field(
        default="SINGLE",
        description="Type of question, either a single question or a multi-question merge",
    )


class QueryPlan(BaseModel):
    """Container class representing a tree of questions to ask a question answering system."""

    query_graph: List[Query] = Field(
        ..., description="The query graph representing the plan"
    )

    def _dependencies(self, ids: List[int]) -> List[Query]:
        """Returns the dependencies of a query given their ids."""
        return [q for q in self.query_graph if q.id in ids]


def query_planner(question: str, model="openai") -> QueryPlan:
    messages = [
        Message(
            role="system",
            content="You are a world class query planning algorithm capable of breaking apart questions into its dependency queries such that the answers can be used to inform the parent question. Do not answer the questions, simply provide a correct compute graph with good specific questions to ask and relevant dependencies. Before you call the function, think step-by-step to get a better understanding of the problem.",
        ),
        Message(
            role="user",
            content=f"Consider: {question}\nGenerate the correct query plan.",
        ),
    ]

    request = CompletionRequest(
        model=get_default_model(model),
        temperature=0,
        response_format=QueryPlan,
        messages=messages,
        max_tokens=1000,
    )
    result = get_completion(model, request)
    plan = result.parsed
    for query in plan.query_graph:
        print(query)


if __name__ == "__main__":
    print("+-+" * 10)
    print("OpenAI")
    query_planner(
      "What is the difference in populations of Canada and the Jason's home country?"
      "openai",
    )
    print("+-+" * 10)
    print("Gemini")
    query_planner(
        "What is the difference in populations of Canada and the Jason's home country?"
        "gemini",
    )
    print("+-+" * 10)
    print("Anthropic")
    query_planner(
        "What is the difference in populations of Canada and the Jason's home country?"
        "anthropic",
    )

