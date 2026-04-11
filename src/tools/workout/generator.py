from .models import WorkoutPlan

def generate_plan(llm_response: str) -> WorkoutPlan:
    # takes the LLM's response and parses it into a WorkoutPlan object
    # hint: think about what format you want the LLM to respond in to make this easier
    pass