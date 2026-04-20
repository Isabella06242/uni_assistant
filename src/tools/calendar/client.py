from composio import Composio
from composio_langchain import LangchainProvider
from dotenv import load_dotenv
import os

load_dotenv()

def get_calendar_tools(user_id: str = "default"):
    """Get Google Calendar tools from Composio using the v3 API."""
    composio = Composio(
        provider=LangchainProvider(),
        api_key=os.getenv("COMPOSIO_API_KEY"),
    )
    return composio.tools.get(user_id=user_id, toolkits=["googlecalendar"], limit=100)
