import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Jaypulse", page_icon="💪", layout="centered")
st.title("Jaypulse — Your Personal Assistant")
st.caption("Ask about workouts or manage your calendar.")

# keep track of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

WORKOUT_KEYWORDS = {"workout", "exercise", "fitness", "muscle", "strength", "cardio",
                    "training", "train", "build", "gain", "lose weight", "bulk", "cut",
                    "plan", "routine", "gym", "push", "pull", "squat", "bench"}

CALENDAR_KEYWORDS = {"schedule", "meeting", "event", "appointment", "add", "create",
                     "list", "show", "delete", "remove", "cancel", "calendar",
                     "tomorrow", "today", "monday", "tuesday", "wednesday", "thursday",
                     "friday", "saturday", "sunday", "pm", "am"}

def detect_intent(text: str) -> str:
    words = set(text.lower().split())
    workout_score = len(words & WORKOUT_KEYWORDS)
    calendar_score = len(words & CALENDAR_KEYWORDS)
    if calendar_score >= workout_score and calendar_score > 0:
        return "calendar"
    if workout_score > 0:
        return "workout"
    return "unknown"

def detect_calendar_action(text: str) -> str:
    lower = text.lower()
    if any(w in lower for w in ["list", "show", "what", "upcoming", "events"]):
        return "list"
    if any(w in lower for w in ["delete", "remove", "cancel"]):
        return "delete"
    return "create"

def format_workout_plan(plan) -> str:
    lines = [f"**Goal:** {plan.goal}", f"**Days per week:** {plan.days_per_week}", ""]
    for day, exercises in plan.schedule.items():
        lines.append(f"**{day}**")
        for ex in exercises:
            lines.append(f"- **{ex.name}** — {ex.description} | {ex.sets} sets × {ex.reps} reps")
        lines.append("")
    return "\n".join(lines)

def handle_workout(prompt: str) -> str:
    from src.tools.workout.agent import create_workout_plan
    try:
        with st.spinner("Generating your workout plan..."):
            plan = create_workout_plan(prompt)
        return format_workout_plan(plan)
    except Exception as e:
        return f"Could not generate workout plan: {e}"

def handle_calendar(prompt: str) -> str:
    action = detect_calendar_action(prompt)

    if action == "list":
        from src.tools.calendar.operations import list_events
        try:
            with st.spinner("Fetching your calendar..."):
                now = datetime.now()
                result = list_events(now, now + timedelta(days=7))
            if result["success"]:
                return result["message"] or "No events found in the next 7 days."
            return f"Could not fetch events: {result['message']}"
        except Exception as e:
            return f"Calendar error: {e}"

    if action == "delete":
        return "To delete an event, please provide the event ID. (e.g. 'delete event abc123')"

    # default: create
    from src.tools.calendar.parser import extract_event_details
    from src.tools.calendar.operations import create_event
    try:
        details = extract_event_details(prompt)
        with st.spinner("Adding event to your calendar..."):
            result = create_event(
                title=details["title"],
                start_time=details["start"],
                end_time=details["end"],
                description=details.get("description"),
            )
        if result["success"]:
            start_str = details["start"].strftime("%A, %b %d at %I:%M %p")
            end_str = details["end"].strftime("%I:%M %p")
            return (f"Event **{details['title']}** added for {start_str}–{end_str}.\n\n"
                    f"{result['message']}")
        return f"Could not create event: {result['message']}"
    except Exception as e:
        return f"Calendar error: {e}"

# handle user input
if prompt := st.chat_input("e.g. 'I want to build muscle' or 'add meeting tomorrow at 2pm'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    intent = detect_intent(prompt)

    with st.chat_message("assistant"):
        if intent == "workout":
            response = handle_workout(prompt)
        elif intent == "calendar":
            response = handle_calendar(prompt)
        else:
            response = ("I'm not sure what you need. Try:\n"
                        "- **Workout:** 'I want to build muscle 3 days a week'\n"
                        "- **Calendar:** 'Add a meeting tomorrow at 2pm for 1 hour'")
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
