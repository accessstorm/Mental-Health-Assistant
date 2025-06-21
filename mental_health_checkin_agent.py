"""
Mental Health Check-In Agent (Terminal Version)

This script is your digital well-being buddy, designed to check in with you about your mental health. It asks how you're feeling, analyzes your response using advanced AI, and offers supportive suggestions. After the initial check-in, you can choose to receive further comforting assistance or a detailed, research-style analysis of your condition. The agent is empathetic, non-judgmental, and always here to help you reflect and feel supported—right from your terminal.

Features:
- Scheduled check-ins (9:00 AM and 8:00 PM)
- AI-powered mood analysis and suggestions
- Options for further assistance or detailed analysis
- Friendly, human-like interaction

To use: Run the script, follow the prompts, and let your digital companion support your mental well-being.
"""
import os
import time
import schedule
from rich.console import Console
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file if present
load_dotenv()

# Set up console for pretty printing
console = Console()

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

def check_in():
    console.rule("[bold green]Mental Health Check-In[/bold green]")
    console.print("How are you feeling right now? (Type your response and press Enter)", style="bold cyan")
    user_input = input("> ")
    console.print("\nAnalyzing your response...", style="yellow")
    try:
        analysis = analyze_mood(user_input)
        console.print(f"\n[bold magenta]Your Check-In Result:[/bold magenta]\n{analysis}")
    except Exception as e:
        console.print(f"[red]Error analyzing response: {e}[/red]")
        return
    console.print("\nThank you for checking in! Remember, you matter.\n", style="bold green")

    # Follow-up options
    while True:
        console.print("\nWhat would you like to do next?", style="bold cyan")
        console.print("[1] Further Assistance\n[2] Detailed Analysis\n[3] Exit", style="bold yellow")
        choice = input("> ").strip()
        if choice == "1":
            console.print("\n[bold blue]Further Assistance:[/bold blue]")
            with console.status("Offering further assistance..."):
                try:
                    followup = further_assistance(user_input)
                    console.print(followup, style="white")
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
        elif choice == "2":
            console.print("\n[bold blue]Detailed Analysis:[/bold blue]")
            with console.status("Generating detailed analysis..."):
                try:
                    followup = detailed_analysis(user_input)
                    console.print(followup, style="white")
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
        elif choice == "3":
            console.print("[bold green]Goodbye! Take care of yourself.[/bold green]")
            break
        else:
            console.print("[red]Invalid choice. Please select 1, 2, or 3.[/red]")

def main():
    console.print("[bold blue]Welcome to your Mental Health Check-In Agent![/bold blue]")
    console.print("This agent will check in with you every morning at 9:00 AM and evening at 8:00 PM. Press Ctrl+C to exit.\n", style="cyan")
    # Schedule check-ins
    schedule.every().day.at("09:00").do(check_in)
    schedule.every().day.at("20:00").do(check_in)
    # For demo: run check-in immediately
    check_in()
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main() 