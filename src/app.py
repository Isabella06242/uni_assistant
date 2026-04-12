import streamlit as st

st.title("Jaypulse — Your personal assistant")

# keep track of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# handle user input
if prompt := st.chat_input("Tell me your fitness goal..."):
    # display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # TODO: figure out if the user is asking about their calendar or workout
    # hint: look at the user's message and decide which agent to call
    # e.g. "add a meeting tomorrow" → calendar agent
    #      "I want to build muscle" → workout agent
    response = "TODO: detect intent and route to the right agent(calendar or workout)"
    
    # display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()