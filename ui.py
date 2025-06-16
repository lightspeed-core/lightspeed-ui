import streamlit as st
import requests
import uuid

st.title("Chat")

# Set or get a persistent conversation ID
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Initalize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build the request payload
    payload = {
            "attachments": [],
            "conversation_id": st.session_state.conversation_id,
            "model": "gpt-4-turbo",
            "provider": "openai",
            "query": prompt,
            "system_prompt": "You are a helpful assistant"
            }

    try:
        # Send POST request
        response = requests.post("http://localhost:8080/v1/query", json=payload)
        response.raise_for_status()
        assistant_reply = response.json().get("response", "Sorry, no response received.")

    except requests.exceptions.RequestException as e:
        assistant_reply = f"Error: {e}"


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


