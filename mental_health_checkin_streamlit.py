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

def get_mood_from_response(analysis_text):
    """Extract mood from AI analysis response."""
    try:
        # Look for "Mood:" in the response
        if "Mood:" in analysis_text:
            mood_line = analysis_text.split("Mood:")[1].split("\n")[0].strip()
            return mood_line
        else:
            # Fallback: try to extract mood from common patterns
            mood_keywords = ["Positive", "Neutral", "Stressed", "Sad", "Anxious", "Happy", "Depressed", "Excited", "Tired", "Energetic"]
            for keyword in mood_keywords:
                if keyword.lower() in analysis_text.lower():
                    return keyword
        return "Unknown"
    except:
        return "Unknown"

def analyze_mood_with_history(user_input):
    """Analyze mood with context from previous check-ins."""
    history = get_user_history()
    recent_moods = []
    
    # Get last 3 moods for context
    if history:
        recent_entries = history[-3:]
        recent_moods = [entry.get("mood", "Unknown") for entry in recent_entries]
    
    # Create enhanced prompt with mood history
    mood_context = ""
    if recent_moods:
        mood_context = f"\n\nUser's recent moods were: {', '.join(recent_moods)}. Please consider this context when analyzing their current state and provide personalized suggestions."
    
    prompt = f"""
You are a friendly mental health companion. Analyze the following user response for signs of stress, sadness, or low mood. Then, suggest a simple, positive action or resource. Be supportive and non-judgmental.

User response: "{user_input}"{mood_context}

Reply with:
Mood: (e.g., Positive, Neutral, Stressed, Sad, Anxious, etc.)
Suggestion: (one actionable, positive suggestion or resource)
"""
    
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
    """Provide further assistance with mood history context."""
    history = get_user_history()
    recent_moods = []
    
    if history:
        recent_entries = history[-3:]
        recent_moods = [entry.get("mood", "Unknown") for entry in recent_entries]
    
    mood_context = ""
    if recent_moods:
        mood_context = f"\n\nUser's recent moods were: {', '.join(recent_moods)}. Please consider this pattern when offering assistance."
    
    prompt = f"""
You are a compassionate mental health companion. The user has asked for further assistance after sharing their feelings. Respond with a comprehensive, comforting, and human-like message, offering emotional support and practical advice. Be empathetic and reassuring.

User's initial message: "{user_input}"{mood_context}
"""
    
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
    """Provide detailed analysis with mood history context."""
    history = get_user_history()
    recent_moods = []
    
    if history:
        recent_entries = history[-3:]
        recent_moods = [entry.get("mood", "Unknown") for entry in recent_entries]
    
    mood_context = ""
    if recent_moods:
        mood_context = f"\n\nUser's recent moods were: {', '.join(recent_moods)}. Please consider this pattern in your analysis."
    
    prompt = f"""
You are a mental health expert. Provide a detailed, research-style analysis of the user's mental health condition based on their message. Include possible causes, effects, and evidence-based strategies for improvement. Use a professional but accessible tone.

User's message: "{user_input}"{mood_context}
"""
    
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Mental Health Check-In Agent", 
        page_icon="🧠",
        layout="wide"
    )
    
    # Initialize session state
    if 'checkin_done' not in st.session_state:
        st.session_state['checkin_done'] = False
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''
    if 'analysis' not in st.session_state:
        st.session_state['analysis'] = ''
    if 'followup' not in st.session_state:
        st.session_state['followup'] = ''
    
    # Header
    st.title("🧠 Mental Health Check-In Agent")
    st.markdown("**Your proactive digital well-being companion** 💙")
    
    # Sidebar for settings and stats
    with st.sidebar:
        st.header("⚙️ Agent Settings")
        
        # Email configuration
        st.subheader("📧 Email Notifications")
        email_config = get_email_config()
        
        email_enabled = st.checkbox("Enable Email Notifications", email_config.get("enabled", False))
        if email_enabled:
            sender_email = st.text_input("Sender Email", email_config.get("sender_email", ""))
            sender_password = st.text_input("Sender Password", email_config.get("sender_password", ""), type="password")
            recipient_email = st.text_input("Recipient Email", email_config.get("recipient_email", ""))
            
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
                    setup_scheduled_emails()
                    st.success("Email settings saved!")
        
        # Check-in interval
        st.subheader("⏰ Check-In Schedule")
        if 'interval' not in st.session_state:
            st.session_state['interval'] = CHECK_IN_INTERVAL_HOURS
        interval = st.slider("Email Check-In Interval (hours)", 2, 5, st.session_state['interval'])
        if interval != st.session_state['interval']:
            st.session_state['interval'] = interval
            setup_scheduled_emails()
        
        # Test email
        if email_enabled:
            if st.button("Send Test Email"):
                if send_checkin_email():
                    st.success("Test email sent!")
                else:
                    st.error("Failed to send test email")
        
        st.markdown("---")
        
        # Stats
        st.subheader("📊 Your Stats")
        history = get_user_history()
        if history:
            total_checkins = len(history)
            st.metric("Total Check-ins", total_checkins)
            
            last_checkin = get_last_checkin()
            if last_checkin:
                last_checkin_dt = datetime.datetime.fromisoformat(last_checkin)
                hours_ago = (datetime.datetime.now() - last_checkin_dt).total_seconds() / 3600
                st.metric("Hours Since Last Check-in", f"{hours_ago:.1f}")
                
                if hours_ago > 24:
                    st.warning("⚠️ It's been over 24 hours since your last check-in. I'm here when you're ready!")
        else:
            st.info("No check-ins yet. Welcome! 👋")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Check-in form
        if not st.session_state['checkin_done']:
            st.subheader("How are you feeling today?")
            
            # Proactive message based on inactivity
            last_checkin = get_last_checkin()
            if last_checkin:
                last_checkin_dt = datetime.datetime.fromisoformat(last_checkin)
                hours_ago = (datetime.datetime.now() - last_checkin_dt).total_seconds() / 3600
                if hours_ago > 24:
                    st.info("💙 Welcome back! I've missed you. How have you been feeling?")
                elif hours_ago > 12:
                    st.info("💙 Good to see you again! How are you doing?")
            
            with st.form("checkin_form"):
                user_input = st.text_area(
                    "Share your thoughts and feelings...", 
                    "", 
                    height=120,
                    placeholder="I'm feeling... (share as much or as little as you'd like)"
                )
                submitted = st.form_submit_button("Check In 💙")
            
            if submitted and user_input.strip():
                with st.spinner("Analyzing your response..."):
                    try:
                        analysis = analyze_mood_with_history(user_input)
                        mood = get_mood_from_response(analysis)
                        
                        # Save to history
                        history = get_user_history()
                        new_entry = {
                            "timestamp": datetime.datetime.now().isoformat(),
                            "mood": mood,
                            "response": user_input,
                            "analysis": analysis
                        }
                        history.append(new_entry)
                        save_user_history(history)
                        
                        # Update last check-in
                        save_last_checkin()
                        
                        st.session_state['analysis'] = analysis
                        st.session_state['user_input'] = user_input
                        st.session_state['checkin_done'] = True
                        st.session_state['mood'] = mood
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error analyzing response: {e}")
        
        # Show result and follow-up options
        if st.session_state['checkin_done']:
            st.success("✅ Check-In Complete!")
            st.markdown(
                f"<div style='background-color:#f0f2f6;padding:1.5em;border-radius:10px;font-size:1.1em;white-space:pre-wrap;word-break:break-word;color:#111;border-left:4px solid #4CAF50;'>" +
                st.session_state['analysis'] + "</div>",
                unsafe_allow_html=True
            )
            
            st.info("💙 Thank you for checking in! Your feelings matter, and I'm here to support you.")
            
            # Follow-up options
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🤗 Further Assistance", use_container_width=True):
                    with st.spinner("Offering further assistance..."):
                        st.session_state['followup'] = further_assistance(st.session_state['user_input'])
            with col_b:
                if st.button("📊 Detailed Analysis", use_container_width=True):
                    with st.spinner("Generating detailed analysis..."):
                        st.session_state['followup'] = detailed_analysis(st.session_state['user_input'])
            
            # Show follow-up response
            if st.session_state['followup']:
                st.markdown(
                    f"<div style='background-color:#e6f7ff;padding:1.5em;border-radius:10px;font-size:1.05em;white-space:pre-wrap;word-break:break-word;color:#111;border-left:4px solid #2196F3;'>" +
                    st.session_state['followup'] + "</div>",
                    unsafe_allow_html=True
                )
            
            # Option to restart
            st.markdown("---")
            if st.button("🔄 Start New Check-In"):
                st.session_state['checkin_done'] = False
                st.session_state['user_input'] = ''
                st.session_state['analysis'] = ''
                st.session_state['followup'] = ''
                st.rerun()
    
    with col2:
        # Mood history chart
        st.subheader("📈 Your Mood Journey")
        history = get_user_history()
        
        if history:
            # Create mood chart
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Count mood frequencies
            mood_counts = df['mood'].value_counts()
            
            # Create pie chart
            fig = px.pie(
                values=mood_counts.values,
                names=mood_counts.index,
                title="Mood Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=300, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent check-ins
            st.subheader("📝 Recent Check-ins")
            recent_entries = history[-5:]  # Last 5 entries
            for entry in reversed(recent_entries):
                timestamp = datetime.datetime.fromisoformat(entry['timestamp'])
                mood = entry.get('mood', 'Unknown')
                response = entry.get('response', '')[:50] + "..." if len(entry.get('response', '')) > 50 else entry.get('response', '')
                
                st.markdown(f"""
                **{timestamp.strftime('%b %d, %H:%M')}** - {mood}
                *"{response}"*
                ---
                """)
        else:
            st.info("No mood data yet. Start your first check-in! 🌟")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9em;'>
        💙 Your Mental Health Companion | Always here to support you
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    # Set up scheduled tasks
    setup_scheduled_emails()
    
    # Check for inactivity (run once on startup)
    check_inactivity()
    
    # Run the main app
    main() 