import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/chat/"

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #F6F6F6;
    }
    .nav-bar {
        background-color: #8785A2;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 10px;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Bar
st.markdown('<div class="nav-bar">Reg No: 12306508 | Name: Aleena Rose Parokkaran</div>', unsafe_allow_html=True)

# Centered App Title
st.markdown('<div class="title">🤖 AIML Chatbot Tutor</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask me anything about <b>Artificial Intelligence & Machine Learning!</b></p>', unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(text)

# User input
user_input = st.chat_input("Ask a question about AIML...")

if user_input:
    # Display user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to FastAPI backend
    response = requests.post(API_URL, json={"message": user_input})

    if response.status_code == 200:
        bot_reply = response.json()["response"]
    else:
        bot_reply = "❌ Error: Unable to fetch response."

    # Display bot response
    st.session_state.messages.append(("assistant", bot_reply))
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
