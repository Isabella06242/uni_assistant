from dataclasses import dataclass
from typing import Optional

@dataclass
class Exercise:
  name: str
  description: str
  sets: int
  reps: int

  def validate(self):
    if not self.name:
      raise ValueError("Exercise must have a name")
    if not self.description:
      raise ValueError(f"{self.name} must have a description")
    if self.sets < 1:
      raise ValueError(f"{self.name} must have at least 1 set")
    if self.reps < 1:
      raise ValueError(f"{self.name} must have at least 1 rep")
    return True

@dataclass
class WorkoutPlan:
  goal: str
  days_per_week: int
  schedule: dict  # {"Monday": [Exercise, ...], ...}

  def validate(self):
    if not self.goal:
      raise ValueError("Workout plan must have a goal")
    if self.days_per_week < 1 or self.days_per_week > 7:
      raise ValueError("Days per week must be between 1 and 7")
    if not self.schedule:
      raise ValueError("Workout plan must have a schedule")
    if self.days_per_week != len(self.schedule):
      raise ValueError("Days per week must match the number of days in the schedule")
    for day, exercises in self.schedule.items():
      if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        raise ValueError(f"Invalid day: {day}")
      if not exercises:
        raise ValueError(f"{day} must have at least one exercise")
      for exercise in exercises:
        exercise.validate()
    return True

  def to_summary(self) -> str:
    summary = f"Workout Plan: {self.goal}\n"
    summary += f"Days per week: {self.days_per_week}\n"
    for day, exercises in self.schedule.items():
      summary += f"{day}:\n"
      for exercise in exercises:
        summary += f"  - {exercise.name}: {exercise.sets} sets x {exercise.reps} reps\n"
    return summary