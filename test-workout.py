from src.tools.workout.models import Exercise, WorkoutPlan
from src.tools.workout.generator import generate_plan
from src.tools.workout.agent import create_workout_plan

# --- Test Exercise model ---
print("=== Exercise model ===")
ex = Exercise(name="Push-up", description="Chest exercise", sets=3, reps=10)
print(ex)

try:
    Exercise(name="", description="desc", sets=3, reps=10)
except ValueError as e:
    print(f"Expected error: {e}")

try:
    Exercise(name="Squat", description="Leg exercise", sets=0, reps=10)
except ValueError as e:
    print(f"Expected error: {e}")

# --- Test WorkoutPlan model ---
print("\n=== WorkoutPlan model ===")
plan = WorkoutPlan(
    goal="Build muscle",
    days_per_week=2,
    schedule={
        "Monday": [
            Exercise(name="Bench Press", description="Chest compound", sets=4, reps=8),
            Exercise(name="Tricep Dip", description="Tricep isolation", sets=3, reps=12),
        ],
        "Thursday": [
            Exercise(name="Squat", description="Leg compound", sets=4, reps=8),
            Exercise(name="Leg Press", description="Quad isolation", sets=3, reps=12),
        ],
    }
)
print(plan.to_summary())

try:
    WorkoutPlan(goal="Test", days_per_week=2, schedule={"Monday": [ex], "Funday": [ex]})
except ValueError as e:
    print(f"Expected error: {e}")

# --- Test generate_plan (no LLM needed) ---
print("\n=== generate_plan (from JSON string) ===")
mock_response = """
{
  "goal": "Lose weight",
  "days_per_week": 3,
  "schedule": {
    "Monday": [{"name": "Running", "description": "Cardio", "sets": 1, "reps": 1}],
    "Wednesday": [{"name": "Cycling", "description": "Low-impact cardio", "sets": 1, "reps": 1}],
    "Friday": [{"name": "Jump Rope", "description": "HIIT cardio", "sets": 3, "reps": 20}]
  }
}
"""
generated = generate_plan(mock_response)
print(generated.to_summary())

# Test with markdown-fenced JSON
print("=== generate_plan (with markdown fences) ===")
fenced_response = """```json
{
  "goal": "Improve endurance",
  "days_per_week": 1,
  "schedule": {
    "Saturday": [{"name": "Long Run", "description": "Steady state cardio", "sets": 1, "reps": 1}]
  }
}
```"""
generated2 = generate_plan(fenced_response)
print(generated2.to_summary())

# --- Test create_workout_plan (calls LLM) ---
print("\n=== create_workout_plan (LLM call) ===")
result = create_workout_plan("I want to build strength, 3 days a week")
print(result.to_summary())