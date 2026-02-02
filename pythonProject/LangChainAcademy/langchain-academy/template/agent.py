# =============================================================
# SOLUTION: Construction Project Assistant using LangGraph
# =============================================================

import os
from dotenv import load_dotenv
load_dotenv()

# 1. IMPORTS
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# 2. IMPORT TOOLS FROM tools.py
from tools import get_project_status, list_project_tasks, get_weather_forecast

# 3. DEFINE STATE
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 4. CREATE TOOLS LIST AND BIND TO LLM
tools = [get_project_status, list_project_tasks, get_weather_forecast]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

# 5. CREATE CHATBOT NODE
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# 6. CREATE ROUTING FUNCTION
def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 7. BUILD THE GRAPH
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")
builder.add_conditional_edges("chatbot", should_continue)
graph = builder.compile()

# 8. TEST MANUALLY
if __name__ == "__main__":
    print("=== Test 1: Project Status ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="What's the status of PROJ-001?")]
    })
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")

    print("\n=== Test 2: List Tasks ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="What tasks are in PROJ-002?")]
    })
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")

    print("\n=== Test 3: Weather ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="What's the weather at the downtown site?")]
    })
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")