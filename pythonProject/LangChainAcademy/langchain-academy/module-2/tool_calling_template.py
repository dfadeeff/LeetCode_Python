"""
Simple LangGraph Agent with Tool Calling Template
Perfect for interview prep!
"""
import os
# Disable LangSmith tracing BEFORE any imports (removes 403 errors)
os.environ["LANGCHAIN_TRACING_V2"] = "false"

"""
================================================================================
                        KEY CONCEPTS REFERENCE GUIDE
================================================================================

1. STATE SCHEMA
---------------
The State Schema defines the structure of data that flows through your graph.
It's like a "contract" that specifies what fields exist and their types.

Three ways to define a State Schema:

    Option A: TypedDict (most common for agents)
    ---------------------------------------------
    class State(TypedDict):
        messages: list
        user_name: str

    Option B: Dataclass
    -------------------
    @dataclass
    class State:
        messages: list
        user_name: str

    Option C: Pydantic BaseModel (adds validation)
    -----------------------------------------------
    class State(BaseModel):
        messages: list
        user_name: str

Why it matters:
- Nodes receive state and return partial updates
- The schema ensures type safety and documentation
- LangGraph uses it to validate data flow


2. STATE REDUCERS
-----------------
Reducers define HOW state updates are merged when a node returns data.

WITHOUT a reducer (default behavior = OVERWRITE):
    State before: {"count": 5}
    Node returns: {"count": 10}
    State after:  {"count": 10}  # Old value is replaced!

WITH a reducer (e.g., operator.add):
    State before: {"count": 5}
    Node returns: {"count": 10}
    State after:  {"count": 15}  # Values are ADDED!

How to apply a reducer - use Annotated:
    from typing import Annotated
    import operator

    class State(TypedDict):
        count: Annotated[int, operator.add]    # Adds values
        messages: Annotated[list, add_messages] # Special message merger
        items: Annotated[list, operator.add]   # Concatenates lists

The add_messages reducer is special:
- Appends new messages to the list
- Handles message IDs to avoid duplicates
- Can update existing messages by ID


3. COMMON REDUCERS
------------------
    operator.add     -> Adds numbers OR concatenates lists/strings
    add_messages     -> Smart message list handling (from langgraph)
    lambda a, b: b   -> Always use new value (same as no reducer)
    lambda a, b: a   -> Always keep old value (ignore updates)


4. STATE UPDATE FLOW
--------------------
    Initial invoke: {"messages": [HumanMessage("Hi")]}
                            │
                            ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  Node 1 (chatbot) receives full state                       │
    │  Returns: {"messages": [AIMessage("Hello!")]}               │
    │                                                             │
    │  With add_messages reducer:                                 │
    │  State becomes: {"messages": [HumanMessage, AIMessage]}     │
    │  (APPENDED, not replaced!)                                  │
    └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  Node 2 (tools) receives updated state                      │
    │  Returns: {"messages": [ToolMessage("result")]}             │
    │                                                             │
    │  State becomes: {"messages": [Human, AI, Tool]}             │
    └─────────────────────────────────────────────────────────────┘


================================================================================
                              GRAPH FLOW DIAGRAM
================================================================================

    START
      │
      ▼
  ┌─────────┐
  │ chatbot │ ◄─────────┐
  └────┬────┘           │
       │                │
       ▼                │
  has tool calls?       │
       │                │
    yes│    no          │
       │    │           │
       ▼    ▼           │
  ┌───────┐ END         │
  │ tools │─────────────┘
  └───────┘

================================================================================
"""

from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# ================================================================
# STEP 0: LOAD ENVIRONMENT VARIABLES
# ================================================================
# Load .env file from parent directory (where OPENAI_API_KEY is stored)
# This makes os.getenv("OPENAI_API_KEY") available to ChatOpenAI
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


# ================================================================
# STEP 1: DEFINE STATE SCHEMA
# ================================================================
# STATE SCHEMA: Defines the structure of data flowing through the graph.
#
# This uses TypedDict - a dictionary with typed keys.
# Each key in the TypedDict is a "channel" that holds data.
#
# REDUCER EXPLAINED:
# -----------------
# Annotated[list, add_messages] breaks down as:
#   - list          = the type (a list)
#   - add_messages  = the REDUCER function
#
# What the reducer does:
#   - When a node returns {"messages": [new_msg]}
#   - Instead of REPLACING the list, it APPENDS to it
#   - This preserves conversation history!
#
# Without reducer:
#   state["messages"] = [msg1, msg2]
#   node returns {"messages": [msg3]}
#   result: state["messages"] = [msg3]  # Lost msg1 and msg2!
#
# With add_messages reducer:
#   state["messages"] = [msg1, msg2]
#   node returns {"messages": [msg3]}
#   result: state["messages"] = [msg1, msg2, msg3]  # All preserved!

class State(TypedDict):
    messages: Annotated[list, add_messages]  # Reducer = add_messages


# ALTERNATIVE STATE SCHEMAS (for reference):
#
# With multiple fields and different reducers:
# --------------------------------------------
# import operator
#
# class State(TypedDict):
#     messages: Annotated[list, add_messages]  # Appends messages
#     call_count: Annotated[int, operator.add] # Sums integers
#     user_name: str                           # No reducer = overwrite


# ================================================================
# STEP 2: DEFINE TOOLS
# ================================================================
# TOOLS: Functions that the LLM can choose to call.
#
# The @tool decorator:
# - Converts a Python function into a LangChain Tool object
# - Extracts the function signature (parameters, types)
# - Extracts the docstring as the tool description
#
# IMPORTANT: The LLM reads the docstring to decide when to use the tool!
# Write clear, descriptive docstrings.

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In a real app, you'd call a weather API here
    return f"The weather in {city} is sunny, 72°F"


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


# Collect tools into a list
# This list is used for:
# 1. llm.bind_tools(tools) - Tell LLM what tools exist
# 2. ToolNode(tools) - Execute tools when called
tools = [get_weather, add_numbers]


# ================================================================
# STEP 3: CREATE LLM WITH TOOLS BOUND
# ================================================================
# Create the LLM instance (reads OPENAI_API_KEY from environment)
llm = ChatOpenAI(model="gpt-4o-mini")

# BIND TOOLS TO LLM
# -----------------
# bind_tools() does NOT execute tools - it just tells the LLM:
# "Hey, these tools exist. You can request to call them."
#
# After binding, when you invoke the LLM:
# - It may respond with text (normal response)
# - OR it may return tool_calls (requests to execute tools)
#
# The tool_calls are NOT executed automatically!
# That's what ToolNode does (see below).
llm_with_tools = llm.bind_tools(tools)


# ================================================================
# STEP 4: DEFINE NODE FUNCTIONS
# ================================================================
# NODES: Functions that process state and return updates.
#
# Node function signature:
#   def my_node(state: State) -> dict:
#       # ... process state ...
#       return {"key": new_value}  # Partial state update
#
# The returned dict is MERGED into state (using reducers if defined).

def chatbot(state: State):
    """
    The "brain" of the agent - calls the LLM.

    Input: Full state (with message history)
    Output: Dict with new message to add

    The LLM will either:
    - Generate a text response (response.content has text)
    - Request tool calls (response.tool_calls has requests)
    """
    # Pass full message history to LLM
    response = llm_with_tools.invoke(state["messages"])

    # Return new message - add_messages reducer will APPEND it
    return {"messages": [response]}


# TOOLNODE: Pre-built node that executes tool calls
# -------------------------------------------------
# What ToolNode does:
# 1. Looks at the LAST message in state["messages"]
# 2. If it has tool_calls, executes each tool
# 3. Returns ToolMessage objects with results
#
# You don't write this logic yourself - LangGraph provides it!
tool_node = ToolNode(tools)


# ================================================================
# STEP 5: DEFINE ROUTING LOGIC (CONDITIONAL EDGES)
# ================================================================
# CONDITIONAL EDGES: Dynamic routing based on state.
#
# This function is called after a node completes.
# It returns a STRING that matches a node name (or END).
#
# Return values:
# - "tools"  -> Route to the tools node
# - "chatbot" -> Route to the chatbot node
# - END      -> Stop the graph

def should_continue(state: State):
    """
    Routing function: Decides where to go after chatbot.

    Checks if the LLM requested any tool calls:
    - Yes -> Go to "tools" node to execute them
    - No  -> Go to END (LLM gave final answer)
    """
    last_message = state["messages"][-1]

    # tool_calls is a list like:
    # [{"name": "get_weather", "args": {"city": "Paris"}, "id": "call_123"}]
    if last_message.tool_calls:
        return "tools"

    return END


# ================================================================
# STEP 6: BUILD THE GRAPH
# ================================================================
# GRAPH CONSTRUCTION: Connect nodes with edges.
#
# StateGraph(State) creates a builder that:
# - Knows the state schema
# - Validates that nodes return correct types

builder = StateGraph(State)

# ADD NODES
# ---------
# add_node(name, function)
# - name: String identifier used in edges
# - function: The node function to execute
builder.add_node("chatbot", chatbot)
builder.add_node("tools", tool_node)

# ADD EDGES
# ---------
# Three types of edges:

# 1. NORMAL EDGE: Always go from A to B
#    add_edge(source, destination)
builder.add_edge(START, "chatbot")  # Graph starts at chatbot
builder.add_edge("tools", "chatbot")  # After tools, back to chatbot

# 2. CONDITIONAL EDGE: Use a function to decide destination
#    add_conditional_edges(source, routing_function)
#    The routing_function returns the destination node name
builder.add_conditional_edges("chatbot", should_continue)

# Note: should_continue returns either "tools" or END
# LangGraph automatically maps these to the right destinations

# COMPILE
# -------
# Turns the builder into an executable graph.
# After compile(), you can call:
# - graph.invoke(state) - Run to completion
# - graph.stream(state) - Stream node outputs
graph = builder.compile()


# ================================================================
# STEP 7: RUN THE GRAPH
# ================================================================
if __name__ == "__main__":
    print("=== Query that uses a tool ===")

    # INVOKE: Run the graph with initial state
    # ----------------------------------------
    # Input: Initial state dict
    # Output: Final state after graph completes
    #
    # The graph will:
    # 1. chatbot: LLM sees "What's the weather?" -> requests get_weather tool
    # 2. should_continue: tool_calls exist -> route to "tools"
    # 3. tools: Execute get_weather("Paris") -> return result
    # 4. chatbot: LLM sees tool result -> generates final answer
    # 5. should_continue: no tool_calls -> route to END

    result = graph.invoke({
        "messages": [HumanMessage(content="What's the weather in Paris?")]
    })

    # Print the conversation flow
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")

    print("\n=== Query that uses add tool ===")
    result = graph.invoke({
        "messages": [HumanMessage(content="What is 15 + 27?")]
    })
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")


"""
================================================================================
                            QUICK REFERENCE CHEATSHEET
================================================================================

IMPORTS YOU'LL NEED:
    from typing import Annotated
    from typing_extensions import TypedDict
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages
    from langgraph.prebuilt import ToolNode

STATE SCHEMA PATTERN:
    class State(TypedDict):
        messages: Annotated[list, add_messages]  # With reducer
        other_field: str                          # Without reducer (overwrites)

TOOL PATTERN:
    @tool
    def my_tool(param: str) -> str:
        '''Description for the LLM.'''  # <-- LLM reads this!
        return "result"

NODE PATTERN:
    def my_node(state: State) -> dict:
        # Do something with state
        return {"messages": [new_message]}  # Partial update

ROUTING PATTERN:
    def router(state: State) -> str:
        if some_condition:
            return "node_name"
        return END

GRAPH BUILD PATTERN:
    builder = StateGraph(State)
    builder.add_node("name", function)
    builder.add_edge(START, "first_node")
    builder.add_edge("node_a", "node_b")
    builder.add_conditional_edges("node", router_function)
    graph = builder.compile()

RUN PATTERN:
    result = graph.invoke({"messages": [HumanMessage(content="...")]})
"""