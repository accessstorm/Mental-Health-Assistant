"""
Configuration file for Mental Health Check-In Agent

This file contains all the configurable settings for the autonomous agent.
Modify these values to customize the agent's behavior to your preferences.
"""

# ============================================================================
# SCHEDULING CONFIGURATION
# ============================================================================

# Email check-in interval (in hours)
# Range: 2-5 hours recommended
CHECK_IN_INTERVAL_HOURS = 3

# Inactivity threshold (in hours)
# Sends alert if no check-in for this many hours
INACTIVITY_THRESHOLD_HOURS = 12

# ============================================================================
# WEB APP CONFIGURATION
# ============================================================================

# URL of your Streamlit app (for email links)
# Update this to your actual deployment URL
WEB_APP_URL = "http://localhost:8501"

# ============================================================================
# AI CONFIGURATION
# ============================================================================

# Number of recent check-ins to use for context
# Higher values provide more context but may slow responses
MOOD_HISTORY_CONTEXT_SIZE = 3

# Maximum tokens for AI responses
ANALYZE_MAX_TOKENS = 300
ASSISTANCE_MAX_TOKENS = 350
ANALYSIS_MAX_TOKENS = 500

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

# Default SMTP settings
DEFAULT_SMTP_SERVER = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587

# Email templates
CHECKIN_EMAIL_SUBJECT = "🧠 Mental Health Check-In Reminder"
CHECKIN_EMAIL_BODY = """
Hey! Just checking in. How are you feeling today?

Your mental health matters, and I'm here to support you. 
Take a moment to reflect on your feelings and share them with me.

Check in here: {web_app_url}

Take care! 💙
Your Mental Health Companion
"""

INACTIVITY_EMAIL_SUBJECT = "⚠️ We Miss You - Mental Health Check-In"
INACTIVITY_EMAIL_BODY = """
Hi there! 

I noticed you haven't checked in for a while. I'm a bit worried and want to make sure you're doing okay.

Remember, it's completely normal to have ups and downs, and I'm here to support you through all of them.

Please take a moment to check in: {web_app_url}

You're not alone, and your feelings matter. 💙

Your Mental Health Companion
"""

# ============================================================================
# DATA STORAGE CONFIGURATION
# ============================================================================

# Directory for storing data files
DATA_DIRECTORY = "data"

# File names for data storage
USER_HISTORY_FILENAME = "user_history.json"
LAST_CHECKIN_FILENAME = "last_checkin.json"
EMAIL_CONFIG_FILENAME = "email_config.json"
AGENT_LOG_FILENAME = "agent.log"

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Streamlit page configuration
STREAMLIT_PAGE_TITLE = "Mental Health Check-In Agent"
STREAMLIT_PAGE_ICON = "🧠"
STREAMLIT_LAYOUT = "wide"

# Chart configuration
CHART_HEIGHT = 300
RECENT_CHECKINS_DISPLAY_COUNT = 5

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# ============================================================================
# MOOD DETECTION CONFIGURATION
# ============================================================================

# Keywords for mood detection (fallback method)
MOOD_KEYWORDS = [
    "Positive", "Neutral", "Stressed", "Sad", "Anxious", 
    "Happy", "Depressed", "Excited", "Tired", "Energetic",
    "Overwhelmed", "Calm", "Frustrated", "Grateful", "Lonely"
]

# ============================================================================
# PROACTIVE MESSAGING CONFIGURATION
# ============================================================================

# Messages shown based on time since last check-in
WELCOME_BACK_24H_MESSAGE = "💙 Welcome back! I've missed you. How have you been feeling?"
WELCOME_BACK_12H_MESSAGE = "💙 Good to see you again! How are you doing?"

# Warning message for extended inactivity
INACTIVITY_WARNING_MESSAGE = "⚠️ It's been over 24 hours since your last check-in. I'm here when you're ready!"

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================

# Enable debug mode (more verbose logging)
DEBUG_MODE = False

# Auto-save interval for data (in seconds)
AUTO_SAVE_INTERVAL = 60

# Maximum number of check-ins to keep in memory
MAX_HISTORY_ENTRIES = 1000

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_config():
    """Validate configuration values."""
    errors = []
    
    if not (2 <= CHECK_IN_INTERVAL_HOURS <= 5):
        errors.append("CHECK_IN_INTERVAL_HOURS must be between 2 and 5")
    
    if INACTIVITY_THRESHOLD_HOURS < 1:
        errors.append("INACTIVITY_THRESHOLD_HOURS must be at least 1")
    
    if MOOD_HISTORY_CONTEXT_SIZE < 1:
        errors.append("MOOD_HISTORY_CONTEXT_SIZE must be at least 1")
    
    if not WEB_APP_URL:
        errors.append("WEB_APP_URL cannot be empty")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(errors))
    
    return True

# Validate configuration on import
if __name__ != "__main__":
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        raise 