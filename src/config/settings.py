# src/config/settings.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. "
        "Please add it to .env file"
    )

# Create the LLM instance
llm = ChatOpenAI(
    model="gpt-4.1",  # change this line to switch models
    temperature=0.7,
    api_key=OPENAI_API_KEY
)

# Optional: function to get different models
def get_llm(model="gpt-4.1", temperature=0.7):
    """Get a customized LLM instance"""
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=OPENAI_API_KEY
    )