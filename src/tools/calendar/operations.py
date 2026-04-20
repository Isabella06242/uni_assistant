from datetime import datetime
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from .client import get_calendar_tools
import os


def _build_agent():
    tools = get_calendar_tools()
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    return create_agent(llm, tools)


def _run_agent(prompt: str) -> str:
    agent = _build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return result["messages"][-1].content


def create_event(
    title: str,
    start_time: datetime,
    end_time: datetime,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[list] = None,
) -> dict:
    try:
        parts = [f"Create a Google Calendar event titled '{title}'",
                 f"from {start_time.isoformat()} to {end_time.isoformat()}"]
        if location:
            parts.append(f"at {location}")
        if description:
            parts.append(f"with description: {description}")
        if attendees:
            parts.append(f"with attendees: {', '.join(attendees)}")

        output = _run_agent(" ".join(parts) + ".")
        return {"success": True, "message": output, "event_id": None}
    except Exception as e:
        return {"success": False, "message": f"Failed to create event: {e}", "event_id": None}


def list_events(time_min: datetime, time_max: datetime, max_results: int = 10) -> dict:
    try:
        prompt = (f"List up to {max_results} Google Calendar events "
                  f"between {time_min.isoformat()} and {time_max.isoformat()}. "
                  f"Return event titles and times.")
        output = _run_agent(prompt)
        return {"success": True, "events": [], "message": output}
    except Exception as e:
        return {"success": False, "events": [], "message": f"Failed to list events: {e}"}


def delete_event(event_id: str) -> dict:
    try:
        output = _run_agent(f"Delete the Google Calendar event with ID: {event_id}")
        return {"success": True, "message": output}
    except Exception as e:
        return {"success": False, "message": f"Failed to delete event: {e}"}
