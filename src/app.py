import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to sys.path to enable absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.workout.agent import create_workout_plan
from src.tools.workout.models import WorkoutPlan
from src.tools.calendar.operations import create_event

st.title("Jaypulse — Your personal assistant")

# keep track of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def detect_intent(user_msg: str) -> str:
    """Detect if user is asking about calendar or workout."""
    user_msg = user_msg.lower()
    
    # Calendar keywords
    calendar_keywords = ["meeting", "event", "calendar", "schedule", "appointment", 
                        "tomorrow", "today", "next week", "add event", "reserve", 
                        "book", "time slot", "when", "when can"]
    
    # Workout keywords
    workout_keywords = ["workout", "exercise", "fitness", "train", "muscle", "gym",
                       "routine", "strength", "cardio", "weight loss", "build",
                       "diet"]
    
    calendar_score = sum(word in user_msg for word in calendar_keywords)
    workout_score = sum(word in user_msg for word in workout_keywords)

    # Check for calendar intent
    if calendar_score > workout_score:
        return "calendar"
    
    # Check for workout intent
    if workout_score > 0:
        return "workout"
    
    return "unknown"

# handle user input
if prompt := st.chat_input("Ask me about scheduling or workouts..."):
    # display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Detect intent and route to appropriate agent
    intent = detect_intent(prompt)
    
    # Show loading spinner while processing
    try:
        if intent == "calendar":
            # TODO: Route to calendar agent
        elif intent == "workout":
            # Route to workout agent
            workout_plan: WorkoutPlan = create_workout_plan(prompt)
            response = workout_plan.to_summary()
        else:
            response = "Do you want help with scheduling or workouts?"
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}"
    
    # display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)