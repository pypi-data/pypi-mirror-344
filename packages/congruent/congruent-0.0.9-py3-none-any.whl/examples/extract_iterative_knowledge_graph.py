from typing import List, Optional

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
    nodes: Optional[List[Node]] = Field(..., default_factory=list)
    edges: Optional[List[Edge]] = Field(..., default_factory=list)

    def update(self, other: "KnowledgeGraph") -> "KnowledgeGraph":
        """Updates the current graph with the other graph, deduplicating nodes and edges."""
        return KnowledgeGraph(
            nodes=list(set(self.nodes + other.nodes)),
            edges=list(set(self.edges + other.edges)),
        )

    def draw(self, prefix: str = None):
        dot = Digraph(comment="Knowledge Graph")

        for node in self.nodes:
            dot.node(str(node.id), node.label, color=node.color)

        for edge in self.edges:
            dot.edge(
                str(edge.source), str(edge.target), label=edge.label, color=edge.color
            )
        dot.render(prefix, format="png", view=True)


from graphviz import Digraph


def visualize_knowledge_graph(kg: KnowledgeGraph):
    dot = Digraph(comment="Knowledge Graph")

    # Add nodes
    for node in kg.nodes:
        dot.node(str(node.id), node.label, color=node.color)

    # Add edges
    for edge in kg.edges:
        dot.edge(str(edge.source), str(edge.target), label=edge.label, color=edge.color)

    # Render the graph
    dot.render("knowledge_graph.gv", view=True)


def main(model="openai"):
    text_chunks = [
        "Jason knows a lot about quantum mechanics. He is a physicist. He is a professor",
        "Professors are smart.",
        "Sarah knows Jason and is a student of his.",
        "Sarah is a student at the University of Toronto. and UofT is in Canada",
    ]

    cur_state = KnowledgeGraph()
    num_iterations = len(text_chunks)
    for i, inp in enumerate(text_chunks):
        messages = [
            Message(
                role="system",
                content="""You are an iterative knowledge graph builder.
                You are given the current state of the graph, and you must append the nodes and edges
                to it Do not procide any duplcates and try to reuse nodes as much as possible.""",
            ),
            Message(
                role="user",
                content=f"""Extract any new nodes and edges from the following:
                # Part {i}/{num_iterations} of the input:

                {inp}""",
            ),
            Message(
                role="user",
                content=f"""Here is the current state of the graph:
                {cur_state.model_dump_json(indent=2)}""",
            ),
        ]
        request = CompletionRequest(
            messages=messages,
            model=get_default_model(model),
            max_tokens=8192,
            tools=[KnowledgeGraph],
        )
        response = get_completion(model, request)
        kn = response.tool_calls[0]
        cur_state = cur_state.update(kn)
        cur_state.draw(prefix=f"{model}_iteration_{i}")

    cur_state.draw(prefix=f"{model}_final")


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
