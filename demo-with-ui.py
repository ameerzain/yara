#!/usr/bin/env python3
"""
Demo script for running Yara backend and Chatbot UI together
This script helps you test the complete chatbot system
"""

import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

def print_banner():
    """Print the demo banner."""
    print("""
🎯 Yara - Complete Chatbot System Demo
=======================================
This script will help you run both the Yara backend API and the chatbot UI
for a complete testing experience!
""")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import transformers
        import torch
        print("✅ Backend dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
        print("💡 Please run: pip install -r requirements.txt")
        return False
    
    return True

def start_backend():
    """Start the Yara backend API server."""
    print("🚀 Starting Yara backend API...")
    
    try:
        # Start the backend server in a subprocess
        backend_process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        print("⏳ Waiting for backend to start...")
        time.sleep(5)
        
        # Check if the process is still running
        if backend_process.poll() is None:
            print("✅ Backend server started successfully!")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print("❌ Backend failed to start:")
            print(stderr.decode())
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_ui():
    """Start the chatbot UI server."""
    print("🌐 Starting Chatbot UI...")
    
    try:
        # Change to the UI directory
        ui_dir = Path("chatbot-ui")
        if not ui_dir.exists():
            print("❌ chatbot-ui directory not found!")
            return None
        
        # Start the UI server
        ui_process = subprocess.Popen([
            sys.executable, "start-ui.py"
        ], cwd=ui_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        print("⏳ Waiting for UI server to start...")
        time.sleep(3)
        
        # Check if the process is still running
        if ui_process.poll() is None:
            print("✅ UI server started successfully!")
            return ui_process
        else:
            stdout, stderr = ui_process.communicate()
            print("❌ UI failed to start:")
            print(stderr.decode())
            return None
            
    except Exception as e:
        print(f"❌ Error starting UI: {e}")
        return None

def open_browsers():
    """Open the relevant URLs in the browser."""
    print("🌐 Opening browser windows...")
    
    try:
        # Open backend API docs
        webbrowser.open("http://localhost:8000/docs")
        print("✅ Backend API docs opened")
        
        # Open chatbot UI
        webbrowser.open("http://localhost:8001/index.html")
        print("✅ Chatbot UI opened")
        
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("💡 Please open these URLs manually:")
        print("   Backend API: http://localhost:8000/docs")
        print("   Chatbot UI: http://localhost:8001/index.html")

def show_instructions():
    """Show usage instructions."""
    print("""
📋 Demo Instructions
===================

🎯 **Backend API (Port 8000)**
   • API Documentation: http://localhost:8000/docs
   • Health Check: http://localhost:8000/health
   • System Status: http://localhost:8000/status
   • Meet Yara: http://localhost:8000/

🌐 **Chatbot UI (Port 8001)**
   • Chat Interface: http://localhost:8001/index.html
   • Settings: Click the gear icon in the UI header
   • API Endpoint: Configure to http://localhost:8000/chat

💬 **Testing the Chatbot**
   1. Open the Chatbot UI in your browser
   2. Type a message and press Enter
   3. Watch Yara respond with her friendly personality!
   4. Try different types of questions:
      • "Hello Yara, how are you?"
      • "What was our revenue last quarter?"
      • "Tell me a joke"
      • "Who are you?"

🔧 **Customization**
   • Modify Yara's personality in nlp.py
   • Change UI styling in chatbot-ui/styles.css
   • Add new features in chatbot.js
   • Configure database settings in .env

⚠️  **Important Notes**
   • Keep both terminal windows open
   • Backend must be running for UI to work
   • Press Ctrl+C in each terminal to stop servers
   • Check console for any error messages

🎉 **Have fun chatting with Yara!**
""")

def main():
    """Main demo function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install dependencies first")
        return
    
    print("\n🚀 Starting complete Yara chatbot system...")
    print("=" * 60)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Start UI
    ui_process = start_ui()
    if not ui_process:
        print("❌ Failed to start UI. Exiting.")
        backend_process.terminate()
        return
    
    print("\n🎉 Both servers are running successfully!")
    print("=" * 60)
    
    # Show instructions
    show_instructions()
    
    # Open browsers
    open_browsers()
    
    print("\n🔄 Both servers are running in the background.")
    print("💡 Check the terminal windows for server logs.")
    print("🛑 Press Ctrl+C in each terminal to stop the servers.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
        
        # Clean up processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        if ui_process:
            ui_process.terminate()
            print("✅ UI server stopped")
        
        print("👋 Demo completed. Goodbye!")

if __name__ == "__main__":
    main()
