import streamlit as st
import requests
import uuid
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--model", default="gpt-4-turbo", help="Model to use")
parser.add_argument("--provider", default="openai", help="Provider to use")
args, unknown = parser.parse_known_args()

st.title("Chat")
st.caption(f"Model: {args.model} ({args.provider})")

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
            "model": args.model,
            "provider": args.provider,
            "query": prompt,
            "system_prompt": "You are a helpful assistant"
            }

    try:
        # Send POST request
        response = requests.post("http://localhost:8080/v1/query", json=payload)
        response.raise_for_status()
        response_data = response.json()
        assistant_reply = response_data.get("response", "Sorry, no response received.")
        st.session_state.conversation_id = response_data.get(
                "conversation_id",
                st.session_state.conversation_id)
    except requests.exceptions.RequestException as e:
        assistant_reply = f"Error: {e}"


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


