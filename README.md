# 🧠 Mental Health Check-In Agent

Welcome to your digital well-being companion! This project is designed to support mental health by providing a friendly, AI-powered check-in experience—either in your terminal or through a modern web app.

## 🌟 What is this?
This agent is like a caring friend who checks in with you, listens to how you're feeling, and offers supportive suggestions or detailed insights. It's built for the MindCraft Hackathon, but it's also a great example of how AI can be used for positive, real-world impact.

## 💡 Features
- **Empathetic AI Check-Ins:** The agent asks how you're feeling and analyzes your response using advanced AI (OpenAI GPT-4o via Azure).
- **Supportive Suggestions:** Get actionable, positive advice tailored to your mood.
- **Further Assistance:** Receive a comprehensive, comforting message if you need more support.
- **Detailed Analysis:** Request a research-style, in-depth analysis of your mental health condition.
- **Two Ways to Use:**
  - **Terminal Version:** For those who love the command line.
  - **Web App Version:** A beautiful, user-friendly interface powered by Streamlit.
- **Scheduled Check-Ins:** The terminal version can check in with you every morning and evening automatically.

## 🚀 How to Set Up

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install Requirements
Make sure you have Python 3.8+ installed.
```sh
pip install -r requirements.txt
```

### 3. Add Your OpenAI API Key (Optional)
By default, the provided Azure OpenAI key is used. For your own deployment, set the following environment variable or edit the script:
```
OPENAI_API_KEY=your-key-here
```
You can use a `.env` file or set it in your environment.

## 🖥️ Usage

### Terminal Version
Run the agent in your terminal:
```sh
python mental_health_checkin_agent.py
```
- The agent will ask how you're feeling.
- After the initial check-in, you can choose:
  - Further Assistance (for a comforting, human-like message)
  - Detailed Analysis (for a research-style, in-depth analysis)
  - Exit
- The agent also schedules check-ins at 9:00 AM and 8:00 PM.

### Web App Version
Run the Streamlit app:
```sh
streamlit run mental_health_checkin_streamlit.py
```
- Use your browser to interact with the agent.
- After your check-in, choose further assistance or detailed analysis.
- Enjoy a modern, friendly interface!

## 🏆 Hackathon Context
This project was built for the MindCraft Hackathon as a demonstration of how AI can be used to support mental health in a non-intrusive, autonomous, and empathetic way.

## 🤝 Contributing
Pull requests and suggestions are welcome! If you have ideas for new features or improvements, feel free to open an issue or PR.

## ⚠️ Disclaimer
This agent is **not a substitute for professional mental health care**. If you are in crisis or need urgent help, please reach out to a mental health professional or helpline in your area.

## 📄 License
MIT License

---

*Built with ❤️ for the MindCraft Hackathon* 