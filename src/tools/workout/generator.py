import json
import re
from .models import Exercise, WorkoutPlan

"""Expected JSON schema:
    {
      "goal": str,
      "days_per_week": int,
      "schedule": {
        "<Day>": [
          {"name": str, "description": str, "sets": int, "reps": int},
          ...
        ],
        ...
      }
    }
"""
def generate_plan(llm_response: str) -> WorkoutPlan:
  # Strip markdown code fences if the LLM wrapped the JSON
  cleaned = re.sub(r"^```(?:json)?\s*", "", llm_response.strip(), flags=re.IGNORECASE)
  cleaned = re.sub(r"\s*```$", "", cleaned)

  data = json.loads(cleaned)

  try:
    goal = data["goal"]
    days_per_week = int(data["days_per_week"])
    schedule_data = data["schedule"]
  except KeyError as err:
    raise ValueError(f"Missing field in LLM response: {err}")
  
  schedule: dict[str, list[Exercise]] = {}
  for day, exercises in schedule_data.items():
    day = day.strip().title()
    schedule[day] = []
    for ex in exercises:
      try:
        name=ex["name"]
        description=ex["description"]
        sets=int(ex["sets"])
        reps=int(ex["reps"])
      except KeyError as err:
        raise ValueError(f"Invalid exercise format in {day}: {ex} - missing {err}")
      
      schedule[day].append(Exercise(
        name=name,
        description=description,
        sets=sets,
        reps=reps
      ))

  plan = WorkoutPlan(
    goal=goal,
    days_per_week=days_per_week,
    schedule=schedule
  )

  return plan