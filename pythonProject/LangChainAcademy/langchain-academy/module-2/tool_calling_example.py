from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from typing import Annotated
import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

class BasicState(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f">>> TOOL CALLED with city: {city}")  # Add this line
    return f"the weather in {city} is sunny, 72 degrees"


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


tools = [get_weather, add_numbers]

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)


def chatbot(state: BasicState):
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}



def should_continue(state:BasicState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"

    return END


builder = StateGraph(BasicState)
builder.add_node("chatbot",chatbot)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_edge("tools","chatbot")
builder.add_conditional_edges("chatbot", should_continue)

graph = builder.compile()


if __name__ == "__main__":
   print("=== Query that uses a tool ===")
   result = graph.invoke({
       "messages": [HumanMessage(content="What's the weather in Paris?")]
   })

   # Print the conversation flow
   for msg in result["messages"]:
       print(f"{msg.type}: {msg.content}")

