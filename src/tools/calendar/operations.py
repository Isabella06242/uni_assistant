from datetime import datetime
from typing import Optional
from composio_langchain import ComposioToolSet, App
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .client import get_calendar_toolset, get_calendar_tools
import os


def _build_agent(toolset: ComposioToolSet) -> AgentExecutor:
    """Build a LangChain agent with calendar tools."""
    tools = get_calendar_tools(toolset)

    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that manages Google Calendar events. "
                   "Always confirm the action taken and return relevant event details."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def create_event(
    title: str,
    start_time: datetime,
    end_time: datetime,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[list[str]] = None,
) -> dict:
    """
    Create a Google Calendar event.

    Args:
        title: Event title/summary
        start_time: Event start as a datetime object
        end_time: Event end as a datetime object
        description: Optional event description
        location: Optional location string
        attendees: Optional list of attendee email strings

    Returns:
        dict with keys: success (bool), event_id (str), message (str)
    """
    try:
        toolset = get_calendar_toolset()
        agent = _build_agent(toolset)

        attendee_str = ""
        if attendees:
            attendee_str = f" with attendees: {', '.join(attendees)}"

        prompt = (
            f"Create a Google Calendar event titled '{title}' "
            f"from {start_time.isoformat()} to {end_time.isoformat()}"
            f"{f' at {location}' if location else ''}"
            f"{f' with description: {description}' if description else ''}"
            f"{attendee_str}."
        )

        result = agent.invoke({"input": prompt})

        return {
            "success": True,
            "message": result.get("output", "Event created successfully."),
            "event_id": None,  # parse from result.output if Composio returns it
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to create event: {str(e)}",
            "event_id": None,
        }


def list_events(
    time_min: datetime,
    time_max: datetime,
    max_results: int = 10,
) -> dict:
    """
    List Google Calendar events within a time range.

    Args:
        time_min: Start of the range (datetime)
        time_max: End of the range (datetime)
        max_results: Max number of events to return

    Returns:
        dict with keys: success (bool), events (list), message (str)
    """
    try:
        toolset = get_calendar_toolset()
        agent = _build_agent(toolset)

        prompt = (
            f"List up to {max_results} Google Calendar events "
            f"between {time_min.isoformat()} and {time_max.isoformat()}. "
            f"Return the event titles, times, and event IDs."
        )

        result = agent.invoke({"input": prompt})

        return {
            "success": True,
            "events": [],  # ideally parsed from result["output"]
            "message": result.get("output", ""),
        }

    except Exception as e:
        return {
            "success": False,
            "events": [],
            "message": f"Failed to list events: {str(e)}",
        }


def delete_event(event_id: str) -> dict:
    """
    Delete a Google Calendar event by ID.

    Args:
        event_id: The Google Calendar event ID

    Returns:
        dict with keys: success (bool), message (str)
    """
    try:
        toolset = get_calendar_toolset()
        agent = _build_agent(toolset)

        prompt = f"Delete the Google Calendar event with ID: {event_id}"

        result = agent.invoke({"input": prompt})

        return {
            "success": True,
            "message": result.get("output", "Event deleted successfully."),
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete event: {str(e)}",
        }