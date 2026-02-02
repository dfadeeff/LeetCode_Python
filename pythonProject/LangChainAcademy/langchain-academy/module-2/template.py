from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list, add_messages]


tools = [...]  # Their tools go here
llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)


def chatbot(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def should_continue(state):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")
builder.add_conditional_edges("chatbot", should_continue)
graph = builder.compile()