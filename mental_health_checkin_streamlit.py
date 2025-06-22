"""
Mental Health Check-In Agent (Autonomous Web App Version)

This Streamlit app is your proactive digital well-being companion, designed to act like a real autonomous agent. 
It features scheduled email check-ins, inactivity alerts, memory logging, and intelligent responses based on 
your mood history. The agent is caring, proactive, and always there to support your mental health journey.

Features:
- Scheduled email check-ins every 2-5 hours
- Inactivity alerts if no check-in for 12+ hours
- Memory logging of all check-ins with mood tracking
- Agent-like intelligence using mood history
- Beautiful charts and proactive messaging
- Human-like, supportive interaction

To use: Run the app with Streamlit, share your feelings, and let your digital companion support your mental well-being.
"""
import os
import json
import time
import datetime
import threading
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from apscheduler.schedulers.background import BackgroundScheduler
import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file if present
load_dotenv()

# Configuration
CHECK_IN_INTERVAL_HOURS = 3  # Email check-in interval (configurable 2-5 hours)
INACTIVITY_THRESHOLD_HOURS = 12  # Alert if no check-in for this many hours
WEB_APP_URL = "http://localhost:8501"  # Update this to your actual URL

# File paths for data storage
DATA_DIR = Path("data")
USER_HISTORY_FILE = DATA_DIR / "user_history.json"
LAST_CHECKIN_FILE = DATA_DIR / "last_checkin.json"
EMAIL_CONFIG_FILE = DATA_DIR / "email_config.json"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Get OpenAI API key from environment or hardcoded (for demo)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or '8WxLaoodYxa7XSK2rCiWuP3nqwWUShSUVd5FrjEYSqqROfIwc0qzJQQJ99BFAC77bzfXJ3w3AAABACOGweqQ'

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint="https://mindcraft-kapidhwaj-openai-api-key.openai.azure.com/"
)

# Initialize scheduler for autonomous features
scheduler = BackgroundScheduler()
scheduler.start()

# ============================================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================================

def load_json_file(file_path, default_value=None):
    """Load JSON file with error handling and default values."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        st.warning(f"Could not load {file_path.name}: {e}")
    return default_value if default_value is not None else []

def save_json_file(file_path, data):
    """Save data to JSON file with error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Could not save {file_path.name}: {e}")
        return False

def get_user_history():
    """Load user check-in history."""
    return load_json_file(USER_HISTORY_FILE, [])

def save_user_history(history):
    """Save user check-in history."""
    return save_json_file(USER_HISTORY_FILE, history)

def get_last_checkin():
    """Get timestamp of last check-in."""
    data = load_json_file(LAST_CHECKIN_FILE, {"timestamp": None})
    return data.get("timestamp")

def save_last_checkin():
    """Save current timestamp as last check-in."""
    data = {"timestamp": datetime.datetime.now().isoformat()}
    return save_json_file(LAST_CHECKIN_FILE, data)

def get_email_config():
    """Load email configuration."""
    return load_json_file(EMAIL_CONFIG_FILE, {
        "enabled": False,
        "sender_email": "",
        "sender_password": "",
        "recipient_email": "",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    })

def save_email_config(config):
    """Save email configuration."""
    return save_json_file(EMAIL_CONFIG_FILE, config)

# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================

def send_email(subject, body, recipient_email=None):
    """Send email using configured settings."""
    config = get_email_config()
    
    if not config.get("enabled"):
        st.warning("Email notifications are not configured. Please set up email in the settings.")
        return False
    
    if not recipient_email:
        recipient_email = config.get("recipient_email")
    
    try:
        # Try yagmail first (easier for Gmail)
        if config.get("smtp_server") == "smtp.gmail.com":
            yag = yagmail.SMTP(config["sender_email"], config["sender_password"])
            yag.send(to=recipient_email, subject=subject, contents=body)
            yag.close()
        else:
            # Fallback to smtplib for other servers
            msg = MIMEMultipart()
            msg['From'] = config["sender_email"]
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["sender_email"], config["sender_password"])
            server.send_message(msg)
            server.quit()
        
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def send_checkin_email():
    """Send scheduled check-in email."""
    subject = "🧠 Mental Health Check-In Reminder"
    body = f"""
Hey! Just checking in. How are you feeling today?

Your mental health matters, and I'm here to support you. 
Take a moment to reflect on your feelings and share them with me.

Check in here: {WEB_APP_URL}

Take care! 💙
Your Mental Health Companion
"""
    return send_email(subject, body)

def send_inactivity_alert():
    """Send inactivity alert email."""
    subject = "⚠️ We Miss You - Mental Health Check-In"
    body = f"""
Hi there! 

I noticed you haven't checked in for a while. I'm a bit worried and want to make sure you're doing okay.

Remember, it's completely normal to have ups and downs, and I'm here to support you through all of them.

Please take a moment to check in: {WEB_APP_URL}

You're not alone, and your feelings matter. 💙

Your Mental Health Companion
"""
    return send_email(subject, body)

# ============================================================================
# SCHEDULING FUNCTIONS
# ============================================================================

def setup_scheduled_emails():
    """Set up scheduled email check-ins."""
    # Remove existing jobs
    for job in scheduler.get_jobs():
        if "checkin_email" in job.id:
            scheduler.remove_job(job.id)
    
    # Add new scheduled job
    scheduler.add_job(
        send_checkin_email,
        'interval',
        hours=CHECK_IN_INTERVAL_HOURS,
        id='checkin_email',
        replace_existing=True
    )

def check_inactivity():
    """Check if user has been inactive and send alert if needed."""
    last_checkin = get_last_checkin()
    if last_checkin:
        last_checkin_dt = datetime.datetime.fromisoformat(last_checkin)
        hours_since_checkin = (datetime.datetime.now() - last_checkin_dt).total_seconds() / 3600
        
        if hours_since_checkin > INACTIVITY_THRESHOLD_HOURS:
            send_inactivity_alert()
            # Update last checkin to prevent spam
            save_last_checkin()

# ============================================================================
# AI ANALYSIS FUNCTIONS
# ============================================================================

def get_conversational_response(messages):
    """Get a conversational response from the AI."""
    
    # The system prompt defines the AI's personality
    system_prompt = {
        "role": "system",
        "content": """You are Kai, a warm, empathetic, and friendly AI companion. 
Your primary goal is to be a supportive friend who listens without judgment. 
When a user shares their feelings, do not jump to analysis or suggestions. 
Instead, engage with them conversationally. Ask gentle, open-ended questions to understand them better, 
like 'What's been on your mind?' or 'I'm here to listen if you want to talk more about that.' 
Maintain a continuous, caring conversation. Keep your responses concise and natural, like a real friend texting.
"""
    }
    
    # We need to ensure the system prompt is always the first message
    api_messages = [system_prompt] + messages
    
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=api_messages,
        max_tokens=350
    )
    return response.choices[0].message.content

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Your Friend, Kai", 
        page_icon="💙",
        layout="centered"
    )
    
    # Initialize session state for conversation history
    if 'messages' not in st.session_state:
        # Start with a welcoming message from Kai
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Hey! I'm Kai. I'm here to listen. How are you feeling today?"
        }]
    
    # Header
    st.title("Your Friend, Kai 💙")
    st.markdown("**A friendly ear, always here to listen.**")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Agent Settings")
        
        # Email configuration
        st.subheader("📧 Scheduled Check-Ins")
        st.write("You can still receive scheduled emails to remind you to chat.")
        email_config = get_email_config()
        
        email_enabled = st.checkbox("Enable Email Check-Ins", email_config.get("enabled", False))
        if email_enabled:
            sender_email = st.text_input("Sender Email (e.g., Gmail)", email_config.get("sender_email", ""))
            sender_password = st.text_input("Sender App Password", email_config.get("sender_password", ""), type="password")
            recipient_email = st.text_input("Your Email (Recipient)", email_config.get("recipient_email", ""))
            
            # Check-in interval slider
            st.session_state.interval = st.slider(
                "Email Check-In Interval (hours)", 
                2, 5, 
                CHECK_IN_INTERVAL_HOURS
            )
            
            # Update the global variable if it changes
            if st.session_state.interval != CHECK_IN_INTERVAL_HOURS:
                # This is one of the few cases where a global is managed this way in Streamlit
                # to interact with a background scheduler.
                globals()['CHECK_IN_INTERVAL_HOURS'] = st.session_state.interval
                setup_scheduled_emails()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Email Settings"):
                    new_config = {
                        "enabled": email_enabled,
                        "sender_email": sender_email,
                        "sender_password": sender_password,
                        "recipient_email": recipient_email,
                        "smtp_server": "smtp.gmail.com",
                        "smtp_port": 587
                    }
                    if save_email_config(new_config):
                        setup_scheduled_emails() # Reschedule with new interval if needed
                        st.success("Email settings saved!")
            
            with col2:
                if st.button("Send Test Email"):
                    with st.spinner("Sending test email..."):
                        if send_checkin_email():
                            st.success("Test email sent!")
                        else:
                            st.error("Failed to send test email.")

        st.markdown("---")
        st.info("Your conversation is private and is not stored. It will be cleared when you close this tab.")
        
        if st.button("🔄 Start New Conversation"):
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "Of course. Let's start fresh. What's on your mind?"
            }]
            st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.spinner("Kai is thinking..."):
            try:
                # Pass the conversation history to the AI
                full_response = get_conversational_response(st.session_state.messages)
                
                # Display AI response
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                
                # Add AI response to session state
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Sorry, I ran into a problem: {e}")

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    # The background scheduler for emails can still run
    # It no longer needs to check for inactivity, just send reminders
    setup_scheduled_emails()
    
    # Run the main app
    main() 