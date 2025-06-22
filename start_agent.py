#!/usr/bin/env python3
"""
Startup Script for Mental Health Check-In Agent

This script helps you start both the Streamlit app and the autonomous agent
with a single command. It provides options to run them separately or together.

Usage:
    python start_agent.py                    # Interactive mode
    python start_agent.py --streamlit        # Run only Streamlit app
    python start_agent.py --agent            # Run only autonomous agent
    python start_agent.py --both             # Run both (recommended)
"""

import os
import sys
import subprocess
import threading
import time
import signal
from pathlib import Path

def print_banner():
    """Print a nice banner for the startup."""
    print("""
🧠 Mental Health Check-In Agent (Autonomous Version)
====================================================
Your proactive digital well-being companion

Features:
• Scheduled email check-ins every 2-5 hours
• Inactivity alerts if no check-in for 12+ hours  
• Memory logging and mood tracking
• Agent-like intelligence with personalized responses
• Beautiful charts and analytics

💙 Your mental health matters, and this agent is here to support you.
""")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'streamlit', 'openai', 'pandas', 'plotly', 
        'yagmail', 'apscheduler', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing dependencies: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def create_data_directory():
    """Create the data directory if it doesn't exist."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✅ Data directory ready")

def run_streamlit():
    """Run the Streamlit app."""
    print("🚀 Starting Streamlit app...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "mental_health_checkin_streamlit.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")

def run_autonomous_agent():
    """Run the autonomous agent."""
    print("🤖 Starting autonomous agent...")
    try:
        subprocess.run([
            sys.executable, "autonomous_agent.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Autonomous agent stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running autonomous agent: {e}")

def run_both():
    """Run both the Streamlit app and autonomous agent."""
    print("🚀 Starting both components...")
    
    # Start autonomous agent in a separate thread
    agent_thread = threading.Thread(target=run_autonomous_agent, daemon=True)
    agent_thread.start()
    
    # Give the agent a moment to start
    time.sleep(2)
    
    # Start Streamlit app (this will block)
    run_streamlit()

def interactive_menu():
    """Show interactive menu for component selection."""
    while True:
        print("\n" + "="*50)
        print("What would you like to run?")
        print("1. Streamlit App (Web Interface)")
        print("2. Autonomous Agent (Background Service)")
        print("3. Both (Recommended)")
        print("4. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_streamlit()
            break
        elif choice == "2":
            run_autonomous_agent()
            break
        elif choice == "3":
            run_both()
            break
        elif choice == "4":
            print("👋 Goodbye! Take care of yourself.")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

def main():
    """Main function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create data directory
    create_data_directory()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--streamlit', '-s']:
            run_streamlit()
        elif arg in ['--agent', '-a']:
            run_autonomous_agent()
        elif arg in ['--both', '-b']:
            run_both()
        elif arg in ['--help', '-h']:
            print(__doc__)
        else:
            print(f"❌ Unknown argument: {arg}")
            print("Use --help for usage information")
    else:
        # Interactive mode
        interactive_menu()

if __name__ == "__main__":
    main() 