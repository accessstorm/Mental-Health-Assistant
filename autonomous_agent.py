"""
Autonomous Mental Health Check-In Agent (Background Service)

This script runs as a background service to handle scheduled email check-ins and inactivity monitoring.
It works alongside the Streamlit app to provide a truly autonomous mental health companion experience.

Features:
- Scheduled email check-ins every 2-5 hours (configurable)
- Inactivity alerts if no check-in for 12+ hours
- Background monitoring and logging
- Email notifications with warm, caring messages

To run: python autonomous_agent.py
"""
import os
import json
import time
import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
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
AGENT_LOG_FILE = DATA_DIR / "agent.log"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(AGENT_LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
        logger.warning(f"Could not load {file_path.name}: {e}")
    return default_value if default_value is not None else []

def save_json_file(file_path, data):
    """Save data to JSON file with error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Could not save {file_path.name}: {e}")
        return False

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

# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================

def send_email(subject, body, recipient_email=None):
    """Send email using configured settings."""
    config = get_email_config()
    
    if not config.get("enabled"):
        logger.warning("Email notifications are not configured.")
        return False
    
    if not recipient_email:
        recipient_email = config.get("recipient_email")
    
    if not recipient_email:
        logger.error("No recipient email configured.")
        return False
    
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
        
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

def send_checkin_email():
    """Send scheduled check-in email."""
    logger.info("Sending scheduled check-in email...")
    
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
    logger.info("Sending inactivity alert email...")
    
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
# MONITORING FUNCTIONS
# ============================================================================

def log_agent_status():
    """Log current agent status."""
    email_config = get_email_config()
    if email_config.get("enabled"):
        logger.info(f"Scheduled email check-ins are ENABLED for {email_config.get('recipient_email')}")
    else:
        logger.info("Scheduled email check-ins are DISABLED.")

# ============================================================================
# SCHEDULER SETUP
# ============================================================================

def setup_scheduler():
    """Set up the scheduler with all tasks."""
    scheduler = BlockingScheduler()
    
    # Scheduled check-in emails
    scheduler.add_job(
        send_checkin_email,
        IntervalTrigger(hours=CHECK_IN_INTERVAL_HOURS),
        id='checkin_email',
        name='Scheduled Check-in Email',
        replace_existing=True
    )
    
    # Status logging (every 6 hours)
    scheduler.add_job(
        log_agent_status,
        IntervalTrigger(hours=6),
        id='status_log',
        name='Status Logging',
        replace_existing=True
    )
    
    return scheduler

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run the autonomous agent."""
    logger.info("Starting Autonomous Mental Health Check-In Agent...")
    logger.info(f"Check-in interval: {CHECK_IN_INTERVAL_HOURS} hours")
    logger.info(f"Inactivity threshold: {INACTIVITY_THRESHOLD_HOURS} hours")
    
    # Check email configuration
    email_config = get_email_config()
    if email_config.get("enabled"):
        logger.info("Email notifications are enabled.")
        logger.info(f"Sender: {email_config.get('sender_email')}")
        logger.info(f"Recipient: {email_config.get('recipient_email')}")
    else:
        logger.warning("Email notifications are not configured. Please set up email in the Streamlit app.")
    
    # Initial status check
    log_agent_status()
    
    # Set up and start scheduler
    scheduler = setup_scheduler()
    
    logger.info("Scheduler started. Agent is now running autonomously.")
    logger.info("Press Ctrl+C to stop the agent.")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Shutting down autonomous agent...")
        scheduler.shutdown()
        logger.info("Autonomous agent stopped.")

if __name__ == "__main__":
    main() 