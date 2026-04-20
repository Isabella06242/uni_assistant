"""
Run this script once to connect your Google Calendar to Composio.
Requires COMPOSIO_API_KEY in your .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from composio import Composio
from composio_langchain import LangchainProvider

c = Composio(provider=LangchainProvider(), api_key=os.getenv("COMPOSIO_API_KEY"))
auth = c.auth_configs.create(toolkit="googlecalendar", options={"type": "use_composio_managed_auth"})
req = c.connected_accounts.initiate(user_id="default", auth_config_id=auth.id)
print("Open this URL in your browser to authorize Google Calendar:")
print(req.redirect_url)
