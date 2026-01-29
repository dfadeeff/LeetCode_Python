from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END


class RandomState(TypedDict):
    name: str
    action: Literal["standing","sleeping","working"]

def node_1(state):
    print("---Node 1---")
    return {"name": state['name'] + " is ... "}


def node_2(state):
    print("---Node 2---")
    return {"action": "working"}

builder = StateGraph(RandomState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"name": "Dmitry"})
    print(result)