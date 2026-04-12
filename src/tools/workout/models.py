from dataclasses import dataclass
from typing import Literal

@dataclass
class Exercise:
  name: str
  description: str
  sets: int
  reps: int

  def __post_init__(self):
    if not isinstance(self.name, str) or not self.name.strip():
      raise ValueError("Exercise must have a name")
    if not isinstance(self.description, str) or not self.description.strip():
      raise ValueError(f"{self.name} must have a description")
    if self.sets < 1:
      raise ValueError(f"{self.name} must have at least 1 set")
    if self.reps < 1:
      raise ValueError(f"{self.name} must have at least 1 rep")
  
  def __str__(self):
    return f"{self.name}\n  {self.description}\n  {self.sets} sets x {self.reps} reps"

DAYS = set(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

@dataclass
class WorkoutPlan:
  goal: str
  days_per_week: int
  schedule: dict[str, list[Exercise]]  # {"Monday": [Exercise, ...], ...}

  def __post_init__(self):
    if not isinstance(self.goal, str) or not self.goal.strip():
      raise ValueError("Workout plan must have a goal")
    if self.days_per_week < 1 or self.days_per_week > 7:
      raise ValueError("Days per week must be between 1 and 7")
    if not self.schedule:
      raise ValueError("Workout plan must have a schedule")
    if self.days_per_week != len(self.schedule):
      raise ValueError("Days per week must match the number of days in the schedule")
    for day, exercises in self.schedule.items():
      if day not in DAYS:
        raise ValueError(f"{day} is not a valid day of the week")
      if not exercises:
        raise ValueError(f"{day} must have at least one exercise")
      seen = set()
      for ex in exercises:
        if not isinstance(ex, Exercise):
          raise ValueError(f"All items in the schedule must be Exercise instances")
        if ex.name in seen:
          raise ValueError(f"{ex.name} is duplicated in {day}'s schedule")
        seen.add(ex.name)

  def to_summary(self) -> str:
    summary = f"Workout Plan: {self.goal}\n"
    summary += f"Days per week: {self.days_per_week}\n"
    for day, exercises in self.schedule.items():
      summary += f"{day}:\n"
      for exercise in exercises:
        summary += f"- {exercise}\n\n"
    return summary