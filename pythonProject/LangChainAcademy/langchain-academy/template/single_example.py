from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
load_dotenv()

# State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# Tools
@tool
def get_project_schedule(project_id: str) -> str:
    """Get the construction schedule for a project."""
    return f"Project {project_id}: Foundation (Week 1-2), Framing (Week 3-4), Roofing (Week 5)"

@tool
def check_material_inventory(material: str) -> str:
    """Check inventory levels for construction materials."""
    inventory = {"lumber": 500, "concrete": 200, "steel": 150}
    return f"{material}: {inventory.get(material.lower(), 0)} units"

@tool
def calculate_cost_estimate(task: str, hours: int) -> str:
    """Calculate cost estimate for a construction task."""
    return f"Cost for {task}: ${hours * 75}"


tools = [get_project_schedule, check_material_inventory, calculate_cost_estimate]

# Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)


def call_model(state: AgentState) -> dict:
    return {"messages": [model.invoke(state["messages"])]}


def should_continue(state: AgentState) -> str:
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")

app = graph.compile()


# Run it
if __name__ == "__main__":
    result = app.invoke({
        "messages": [HumanMessage(content="What's the schedule for project ABC123?")]
    })
    print(result["messages"][-1].content)