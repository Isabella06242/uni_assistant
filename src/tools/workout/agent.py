from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

llm = ChatOpenAI(...)  # what model and settings make sense here?

# hint: wrap generate_plan as a LangChain tool
# look at how calendar/agent.py sets this up — same pattern