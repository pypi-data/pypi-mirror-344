from typing import List

from pydantic import BaseModel, Field

from congruent.schemas.completion import CompletionRequest, Message
from examples.utils import get_default_model, get_completion


class Node(BaseModel, frozen=True):
    id: int
    label: str
    color: str


class Edge(BaseModel, frozen=True):
    source: int
    target: int
    label: str
    color: str = "black"


class KnowledgeGraph(BaseModel):
    nodes: List[Node] = Field(..., default_factory=list)
    edges: List[Edge] = Field(..., default_factory=list)

from graphviz import Digraph


def visualize_knowledge_graph(model, kg: KnowledgeGraph):
    dot = Digraph(comment=f"{model} Knowledge Graph")

    # Add nodes
    for node in kg.nodes:
        dot.node(str(node.id), node.label, color=node.color)

    # Add edges
    for edge in kg.edges:
        dot.edge(str(edge.source), str(edge.target), label=edge.label, color=edge.color)

    # Render the graph
    dot.render(f"{model}_knowledge_graph.gv", view=True)


def main(model="openai"):
    question = "Teach me about quantum mechanics"

    messages = [
        Message(
            role="user",
            content=f"Help me understand the following by describing it as a detailed knowledge graph: {question}",
        ),
    ]

    request = CompletionRequest(
        messages=messages,
        model=get_default_model(model),
        max_tokens=8192,
        tools=[KnowledgeGraph],
    )

    response = get_completion(model, request)
    if response.tool_calls:
      kn = response.tool_calls[0]
      visualize_knowledge_graph(model, kn)
    else:
      print(f"No tool calls found in the response for {model}.")


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
