Live link:
https://kai-mentalhealth.streamlit.app/
# Your Friend, Kai 💙

A warm, empathetic, and friendly AI companion. Kai is here to be a supportive friend who listens without judgment. You can talk about your feelings, and Kai will engage in a natural, caring conversation.

This app is designed to feel like a private chat with a friend. Your conversation is **not stored** and will be cleared when you close the browser tab.

## ✨ Features

- **Empathetic AI Companion**: Talk with Kai, an AI designed to be a supportive and friendly ear.
- **Natural Conversation**: Instead of analyzing, Kai engages in a back-and-forth, human-like conversation.
- **Complete Privacy**: Your chat history is only stored for your current session and is deleted when you close the app. No permanent records are kept.
- **Scheduled Email Reminders (Optional)**: If you like, Kai can send you gentle email reminders to encourage you to chat. This is fully configurable and can be disabled.
- **Modern Chat Interface**: A clean, beautiful chat UI powered by Streamlit.

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run mental_health_checkin_streamlit.py
```
This will open the chat interface in your browser.

### 3. Run the Autonomous Email Agent (Optional)
If you want to receive scheduled email reminders, run this agent in a separate terminal:
```bash
python autonomous_agent.py
```
You can configure your email settings in the sidebar of the web app.

---

## ⚙️ Configuration

- **Email Settings**: In the app's sidebar, you can enable email check-ins, provide your email details (using a Gmail App Password is required for security), and save your settings.
- **Privacy**: By default, all conversation data is ephemeral. There is nothing to configure here—your privacy is the default.

## 🧠 The AI's Personality

Kai is instructed to be a friendly companion, not a doctor. The system prompt emphasizes:
- Listening without judgment.
- Asking gentle, open-ended questions.
- Avoiding immediate analysis or suggestions.
- Maintaining a natural, caring, and continuous conversation.

---

**💙 Remember: You're not alone. Kai is here to listen whenever you need a friend.** 