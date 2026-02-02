# =============================================================
# TESTS - Your agent must pass these
# Run with: pytest -v
# =============================================================

import pytest
from langchain_core.messages import HumanMessage


class TestAgentBasics:
    """Basic tests to verify agent structure."""

    def test_graph_exists(self):
        """Test that graph is defined and compiled."""
        from agent import graph
        assert graph is not None

    def test_graph_can_invoke(self):
        """Test that graph can be invoked with a message."""
        from agent import graph
        result = graph.invoke({
            "messages": [HumanMessage(content="Hello")]
        })
        assert "messages" in result
        assert len(result["messages"]) > 0


class TestToolUsage:
    """Tests to verify the agent uses tools correctly."""

    def test_project_status_tool(self):
        """Test that agent uses get_project_status tool."""
        from agent import graph
        result = graph.invoke({
            "messages": [HumanMessage(content="What is the status of project PROJ-001?")]
        })
        # Check that the response mentions the project
        final_response = result["messages"][-1].content
        assert "PROJ-001" in final_response or "45%" in final_response or "progress" in final_response.lower()

    def test_list_tasks_tool(self):
        """Test that agent uses list_project_tasks tool."""
        from agent import graph
        result = graph.invoke({
            "messages": [HumanMessage(content="What are the tasks for PROJ-002?")]
        })
        final_response = result["messages"][-1].content
        assert "task" in final_response.lower() or "foundation" in final_response.lower()

    def test_weather_tool(self):
        """Test that agent uses get_weather_forecast tool."""
        from agent import graph
        result = graph.invoke({
            "messages": [HumanMessage(content="What's the weather forecast for the downtown site?")]
        })
        final_response = result["messages"][-1].content
        assert "weather" in final_response.lower() or "sunny" in final_response.lower()


class TestAgentBehavior:
    """Tests for agent behavior without tools."""

    def test_responds_to_greeting(self):
        """Test that agent responds to simple greeting without using tools."""
        from agent import graph
        result = graph.invoke({
            "messages": [HumanMessage(content="Hi, who are you?")]
        })
        assert len(result["messages"]) >= 2  # At least human + AI response