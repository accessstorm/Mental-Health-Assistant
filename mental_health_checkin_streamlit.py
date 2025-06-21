"""
Mental Health Check-In Agent (Web App Version)

This Streamlit app is your digital well-being companion, designed to check in with you about your mental health in a warm, supportive way. It invites you to share how you're feeling, analyzes your response using advanced AI, and offers empathetic suggestions. After your check-in, you can choose to receive further comforting assistance or a detailed, research-style analysis of your condition. The app is designed to feel human, non-judgmental, and always supportive—right in your browser.

Features:
- Simple, friendly web interface
- AI-powered mood analysis and suggestions
- Options for further assistance or detailed analysis
- Human-like, supportive interaction

To use: Run the app with Streamlit, share your feelings, and let your digital companion support your mental well-being.
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

# Load environment variables from .env file if present
load_dotenv()

# Get OpenAI API key from environment or hardcoded (for demo)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or '8WxLaoodYxa7XSK2rCiWuP3nqwWUShSUVd5FrjEYSqqROfIwc0qzJQQJ99BFAC77bzfXJ3w3AAABACOGweqQ'

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint="https://mindcraft-kapidhwaj-openai-api-key.openai.azure.com/"
)

# Prompt templates
ANALYZE_PROMPT = """
You are a friendly mental health companion. Analyze the following user response for signs of stress, sadness, or low mood. Then, suggest a simple, positive action or resource. Be supportive and non-judgmental.

User response: "{user_input}"

Reply with:
Mood: (e.g., Positive, Neutral, Stressed, Sad, Anxious, etc.)
Suggestion: (one actionable, positive suggestion or resource)
"""

FURTHER_ASSISTANCE_PROMPT = """
You are a compassionate mental health companion. The user has asked for further assistance after sharing their feelings. Respond with a comprehensive, comforting, and human-like message, offering emotional support and practical advice. Be empathetic and reassuring.

User's initial message: "{user_input}"
"""

DETAILED_ANALYSIS_PROMPT = """
You are a mental health expert. Provide a detailed, research-style analysis of the user's mental health condition based on their message. Include possible causes, effects, and evidence-based strategies for improvement. Use a professional but accessible tone.

User's message: "{user_input}"
"""

# Helper functions
def analyze_mood(user_input):
    prompt = ANALYZE_PROMPT.format(user_input=user_input)
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def further_assistance(user_input):
    prompt = FURTHER_ASSISTANCE_PROMPT.format(user_input=user_input)
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=350
    )
    return response.choices[0].message.content

def detailed_analysis(user_input):
    prompt = DETAILED_ANALYSIS_PROMPT.format(user_input=user_input)
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Mental Health Check-In Agent", page_icon="🧠")
st.title("🧠 Mental Health Check-In Agent")
st.write("Welcome! This digital well-being buddy checks in with you and suggests positive actions based on your feelings.")

# Session state for conversation and follow-up
if 'checkin_done' not in st.session_state:
    st.session_state['checkin_done'] = False
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
if 'analysis' not in st.session_state:
    st.session_state['analysis'] = ''
if 'followup' not in st.session_state:
    st.session_state['followup'] = ''

# Initial check-in form
if not st.session_state['checkin_done']:
    with st.form("checkin_form"):
        user_input = st.text_area("How are you feeling right now?", "", height=100)
        submitted = st.form_submit_button("Check In")
    if submitted and user_input.strip():
        with st.spinner("Analyzing your response..."):
            try:
                analysis = analyze_mood(user_input)
                st.session_state['analysis'] = analysis
                st.session_state['user_input'] = user_input
                st.session_state['checkin_done'] = True
            except Exception as e:
                st.error(f"Error analyzing response: {e}")

# Show result and follow-up options
if st.session_state['checkin_done']:
    st.success("Check-In Result:")
    st.markdown(
        f"<div style='background-color:#f0f2f6;padding:1em;border-radius:8px;font-size:1.1em;white-space:pre-wrap;word-break:break-word;color:#111;'>" +
        st.session_state['analysis'] + "</div>",
        unsafe_allow_html=True
    )
    st.info("Thank you for checking in! Remember, you matter.")

    # Follow-up options (only two now)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Further Assistance"):
            with st.spinner("Offering further assistance..."):
                st.session_state['followup'] = further_assistance(st.session_state['user_input'])
    with col2:
        if st.button("Detailed Analysis"):
            with st.spinner("Generating detailed analysis..."):
                st.session_state['followup'] = detailed_analysis(st.session_state['user_input'])

    # Show follow-up response
    if st.session_state['followup']:
        st.markdown(
            f"<div style='background-color:#e6f7ff;padding:1em;border-radius:8px;font-size:1.05em;white-space:pre-wrap;word-break:break-word;color:#111;'>" +
            st.session_state['followup'] + "</div>",
            unsafe_allow_html=True
        )

    # Option to restart
    st.markdown("---")
    if st.button("Start New Check-In"):
        st.session_state['checkin_done'] = False
        st.session_state['user_input'] = ''
        st.session_state['analysis'] = ''
        st.session_state['followup'] = '' 