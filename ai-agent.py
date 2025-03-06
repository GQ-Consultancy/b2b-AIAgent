import streamlit as st
import requests
import json
import os
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

st.set_page_config(page_title="Support Chat Assistant", page_icon="💬", layout="centered")

st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

def send_question_to_webhook(question, webhook_url):
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "question": question
    }
    
    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        if isinstance(response.text, str):
            try:
                response_data = json.loads(response.text)
                return response_data.get('content', response.text)
            except json.JSONDecodeError:
                return response.text
        return response.text
            
    except Exception as e:
        return f"Error: {str(e)}"

def process_question(question):
    with st.chat_message("user"):
        st.markdown(question)
    
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner('Getting response...'):
        response = send_question_to_webhook(question, st.session_state.webhook_url)

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.title("💬 Support Chat Assistant")

# Get webhook URL from environment variable, with fallback for local testing
webhook_url = "https://hook.us2.make.com/ffwwp947qa83gkak0i3aidx8z34o7szy"

if 'webhook_url' not in st.session_state:
    st.session_state.webhook_url = webhook_url
    
    # For development/testing only - show a warning if no webhook URL is configured
    if not webhook_url:
        st.warning("⚠️ No webhook URL configured. Please set the WEBHOOK_URL environment variable.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

example_questions = [
    "How do I reset my password?",
    "What payment methods do you accept?",
    "How do I cancel my subscription?",
    "What are the system requirements?",
    "How do I contact support?"
]

with st.expander("📝 Example Questions"):
    selected_question = st.selectbox(
        "Select a question to try:",
        example_questions
    )
    if st.button("Ask Selected Question"):
        process_question(selected_question)
        st.rerun()

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    process_question(prompt)
