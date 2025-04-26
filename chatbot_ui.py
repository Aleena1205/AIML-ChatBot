import streamlit as st
import requests
import time
import pybase64
API_URL = "http://127.0.0.1:8000/chat/"

st.set_page_config(page_title="Knowva", page_icon="🤖", layout="wide")



# Sidebar- Settings &Chat History
with st.sidebar:
    st.title("⚙️ Settings")
    theme = st.radio("Choose theme", ["Dark", "Light"])
    st.markdown("Made by Aleena Rose(12306508)")

    st.title("🕰️ Chat History")
    for i, session in enumerate(st.session_state.get("chat_sessions", [])):
        if st.button(f"Conversation {i+1}"):
            st.session_state.messages = session.copy()
            st.rerun()
    #new chat
    if st.button("New Chat"):
        if st.session_state.get("messages"):
            st.session_state.chat_sessions.append(st.session_state.messages.copy())
        st.session_state.messages = []
        st.rerun()

# Theme
if theme == "Dark":
    bg_color = "#1e1e2f"
    user_bubble_color = "#2e2e3e"
    bot_bubble_color = "#3e3e4e"
    text_color = "white"
else:
    bg_color = "#fdfbfb"
    user_bubble_color = "#d4eaf7"
    bot_bubble_color = "#f1f0f0"
    text_color = "black"

# CSS styling
st.markdown(
    f"""
    <style>
    body {{
        background: linear-gradient(to right, #a18cd1, #fbc2eb);
        color: {text_color};
        font-family: 'Poppins', sans-serif;
    }}
    .nav-bar {{
        background-color: #8785A2;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 30px;
    }}
    .title {{
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        color: white !important;
        font-family: 'Poppins', sans-serif;
        margin-top: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .subtitle {{
        text-align: center;
        font-size: 1.1rem;
        color: {text_color};
        font-style: italic;
    }}
    button:hover {{
        background-color: #1B56FD !important;
        color: white !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NavBar
#st.markdown('<div class="nav-bar">Reg No: 12306508 | Name: Aleena Rose Parokkaran</div>', unsafe_allow_html=True)

st.markdown('<div class="title">🤖 Knowva</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Hi, I\'m Knowva – your AIML tutor and chatbot guide!</p>', unsafe_allow_html=True)

# Initialize session state for messages and chat sessions
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

# Function to format messages as styled bubbles
def format_message(role, text):
    return f'''
        <div style="background-color:{user_bubble_color if role == "user" else bot_bubble_color};
                    color:{text_color};
                    padding:10px;
                    border-radius:20px;
                    margin:5px 0;
                    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);">
            {"👩🏽‍💼 <b>You:</b>" if role == "user" else "🤖 <b>Knowva:</b>"} {text}
        </div>
    '''

# Display  history
for role, text in st.session_state.messages:
    st.markdown(format_message(role, text), unsafe_allow_html=True)

# User input
user_input = st.chat_input("Ask a question about AIML...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.markdown(format_message("user", user_input), unsafe_allow_html=True)

    typing_placeholder = st.empty()
    typing_placeholder.markdown("🤖 Knowva is typing...")
    time.sleep(1.5)
    typing_placeholder.empty()

    response = requests.post(API_URL, json={"message": user_input})
    if response.status_code == 200:
        bot_reply = response.json().get("response", "❌ Error: No response from server.")
    else:
        bot_reply = "❌ Error: Unable to fetch response."

    st.session_state.messages.append(("assistant", bot_reply))
    st.markdown(format_message("assistant", bot_reply), unsafe_allow_html=True)

# Buttons 
col1, col2 = st.columns(2)
with col1:
    chat_text = "\n\n".join([f"{role.upper()}: {text}" for role, text in st.session_state.messages])
    st.download_button("📥 Download Chat History", chat_text, file_name="chat_history.txt", use_container_width=True)
with col2:
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
