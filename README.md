# 🧠 Mental Health Check-In Agent (Autonomous Version)

A proactive, autonomous digital well-being companion that acts like a real caring agent. This application features scheduled email check-ins, inactivity alerts, memory logging, and intelligent responses based on your mood history.

## ✨ Features

### 🤖 Autonomous Agent Capabilities
- **Scheduled Email Check-Ins**: Receives gentle reminders every 2-5 hours (configurable)
- **Inactivity Alerts**: Gets worried and sends caring emails if you haven't checked in for 12+ hours
- **Memory Logging**: Remembers all your check-ins and mood patterns
- **Agent-Like Intelligence**: Uses your mood history to provide personalized responses
- **Proactive Messaging**: Welcomes you back with warm messages based on your absence

### 📊 Enhanced Analytics
- **Mood Tracking**: Visual charts showing your emotional journey
- **Check-in History**: Complete log of all your interactions
- **Statistics Dashboard**: Total check-ins, time since last check-in, and more
- **Beautiful Visualizations**: Interactive charts using Plotly

### 💌 Email Integration
- **Gmail Support**: Easy setup with Gmail SMTP
- **Custom SMTP**: Support for other email providers
- **Warm, Caring Messages**: Human-like email content
- **Configurable Intervals**: Adjust check-in frequency as needed

### 🎨 Modern UI
- **Streamlit Interface**: Beautiful, responsive web app
- **Real-time Updates**: Live statistics and charts
- **Mobile-Friendly**: Works on all devices
- **Intuitive Design**: Easy to use and navigate

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Email (Optional but Recommended)
1. Open the Streamlit app
2. Go to the sidebar settings
3. Enable email notifications
4. Enter your Gmail credentials (use an app password for security)
5. Add your recipient email
6. Save settings

### 3. Run the Streamlit App
```bash
streamlit run mental_health_checkin_streamlit.py
```

### 4. Run the Autonomous Agent (Background Service)
```bash
python autonomous_agent.py
```

## 📁 File Structure

```
MCP kamala/
├── mental_health_checkin_streamlit.py  # Main Streamlit app
├── autonomous_agent.py                 # Background service
├── mental_health_checkin_agent.py      # Terminal version
├── requirements.txt                    # Dependencies
├── README.md                          # This file
└── data/                              # Data storage (auto-created)
    ├── user_history.json              # Check-in history
    ├── last_checkin.json              # Last check-in timestamp
    ├── email_config.json              # Email settings
    └── agent.log                      # Agent activity log
```

## ⚙️ Configuration

### Email Settings
- **Sender Email**: Your Gmail address
- **Sender Password**: Gmail app password (not regular password)
- **Recipient Email**: Where to send check-in reminders
- **Check-in Interval**: 2-5 hours (configurable)

### Agent Behavior
- **Inactivity Threshold**: 12 hours (configurable)
- **Memory Context**: Uses last 3 check-ins for personalized responses
- **Logging**: Comprehensive activity logging

## 🔧 Advanced Setup

### Gmail App Password Setup
1. Go to your Google Account settings
2. Enable 2-factor authentication
3. Generate an app password for "Mail"
4. Use this password in the email configuration

### Custom SMTP Setup
For non-Gmail providers, modify the email configuration:
```json
{
  "enabled": true,
  "sender_email": "your-email@domain.com",
  "sender_password": "your-password",
  "recipient_email": "recipient@domain.com",
  "smtp_server": "smtp.your-provider.com",
  "smtp_port": 587
}
```

## 📊 Data Storage

All data is stored locally in JSON format:

### User History Format
```json
[
  {
    "timestamp": "2025-01-22T14:30:00",
    "mood": "Sad",
    "response": "I'm feeling overwhelmed...",
    "analysis": "Mood: Sad\nSuggestion: Take a short walk..."
  }
]
```

### Last Check-in Format
```json
{
  "timestamp": "2025-01-22T14:30:00"
}
```

## 🧠 How It Works

### Autonomous Features
1. **Background Monitoring**: The autonomous agent runs continuously
2. **Scheduled Check-ins**: Sends caring emails at regular intervals
3. **Inactivity Detection**: Monitors for extended periods without check-ins
4. **Memory Integration**: Uses historical data for personalized responses

### AI Intelligence
- Analyzes your responses using GPT-4o
- Extracts mood patterns from your text
- Provides context-aware suggestions
- Learns from your interaction history

### Proactive Behavior
- Welcomes you back after absences
- Shows concern for extended inactivity
- Provides warm, human-like interactions
- Adapts responses based on your mood patterns

## 🛠️ Troubleshooting

### Email Issues
- **Gmail**: Use app passwords, not regular passwords
- **Authentication**: Ensure 2FA is enabled for Gmail
- **SMTP**: Check port and server settings for other providers

### Data Issues
- **File Permissions**: Ensure write access to the data directory
- **JSON Corruption**: Delete corrupted files to reset data
- **Path Issues**: Check that the data directory exists

### Agent Issues
- **Scheduler**: Restart the autonomous agent if scheduling fails
- **Logs**: Check `data/agent.log` for detailed error information
- **Configuration**: Verify email settings in the Streamlit app

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally on your machine
- **No Cloud**: No data sent to external servers (except OpenAI API)
- **Email Security**: Use app passwords for Gmail
- **Data Control**: You can delete data files at any time

## 🎯 Use Cases

- **Daily Mental Health Monitoring**: Regular check-ins for emotional well-being
- **Mood Pattern Analysis**: Track emotional trends over time
- **Proactive Support**: Get gentle reminders when needed
- **Personal Growth**: Reflect on feelings and receive guidance
- **Stress Management**: Identify and address stress patterns

## 🤝 Contributing

Feel free to enhance the agent with additional features:
- New mood analysis algorithms
- Additional visualization types
- Integration with other health apps
- Enhanced email templates
- Mobile app version

## 📞 Support

If you encounter issues:
1. Check the logs in `data/agent.log`
2. Verify your email configuration
3. Ensure all dependencies are installed
4. Check file permissions in the data directory

---

**💙 Remember: Your mental health matters, and this agent is here to support you on your well-being journey.** 