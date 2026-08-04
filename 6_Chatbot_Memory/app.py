import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

MODEL_ID = "gemini-3.6-flash"

st.set_page_config(page_title="Mohd Wasim AI Chat", page_icon="💬")
st.title("💬 Chat with Adobe")
st.caption("Memory chatbot - by Mohd Wasim")

# Initialize conversation history in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Sidebar to show conversation raw
with st.sidebar:
    st.header("Conversation History")
    if st.button("Clear Chat"):
        st.session_state.conversation = []
        st.rerun()
    for msg in st.session_state.conversation:
        st.text(f"{msg['role']} -> {msg['parts'][0]['text'][:100]}")

def chat(user_message):
    st.session_state.conversation.append({"role": "user", "parts": [{"text": user_message}]})
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=st.session_state.conversation
        )
        reply = response.text
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

    st.session_state.conversation.append({"role": "model", "parts": [{"text": reply}]})
    return reply

# Display chat messages
for message in st.session_state.conversation:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(message["parts"][0]["text"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.write(prompt)

    reply = chat(prompt)

    with st.chat_message("assistant"):
        st.write(reply)