from composio_langchain import ComposioToolSet, App
from dotenv import load_dotenv
import os

load_dotenv()

def get_calendar_toolset() -> ComposioToolSet:
    """Initialize and return a Composio toolset with Google Calendar tools."""
    toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
    return toolset

def get_calendar_tools(toolset: ComposioToolSet = None):
    """Get the Google Calendar tools from Composio."""
    if toolset is None:
        toolset = get_calendar_toolset()
    
    tools = toolset.get_tools(apps=[App.GOOGLECALENDAR])
    return tools