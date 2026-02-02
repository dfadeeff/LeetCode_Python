# PROVIDED BY INTERVIEWER - Do not modify
from langchain_core.tools import tool


@tool
def get_project_status(project_id: str) -> str:
    """Get the current status of a construction project by its ID."""
    projects = {
        "PROJ-001": "In Progress - 45% complete, on schedule",
        "PROJ-002": "Delayed - 30% complete, 2 weeks behind",
        "PROJ-003": "Completed - 100% complete, delivered on time",
    }
    return projects.get(project_id, f"Project {project_id} not found")


@tool
def list_project_tasks(project_id: str) -> str:
    """List all tasks for a given construction project."""
    tasks = {
        "PROJ-001": "1. Foundation (done), 2. Framing (in progress), 3. Roofing (pending)",
        "PROJ-002": "1. Site prep (done), 2. Foundation (delayed), 3. Framing (pending)",
        "PROJ-003": "1. Foundation (done), 2. Framing (done), 3. Roofing (done), 4. Interior (done)",
    }
    return tasks.get(project_id, f"No tasks found for {project_id}")


@tool
def get_weather_forecast(location: str) -> str:
    """Get weather forecast for a construction site location."""
    return f"Weather in {location}: Sunny, 72°F, no rain expected for 5 days. Good conditions for construction."