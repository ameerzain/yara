#!/usr/bin/env python3
"""
Demo script for the Intelligent Chatbot API.
Showcases the chatbot's capabilities with interactive examples.
"""

import asyncio
import json
import time
from typing import Dict, Any

def print_header():
    """Print demo header."""
    print("""
🎯 Meet Yara - Your Friendly AI Assistant Demo
==============================================
This demo showcases Yara's amazing capabilities:
1. General Chat Mode - Natural, friendly conversations using LLM
2. Database Mode - Organization-specific data queries with enthusiasm

Yara is excited to meet you and help with anything you need! ✨

Press Ctrl+C to exit the demo
""")

def print_examples():
    """Print example queries for users to try."""
    print("💡 Try these example queries with Yara:")
    print()
    
    print("📊 Database Queries (if database is connected):")
    print("  • 'What was our revenue last quarter?'")
    print("  • 'How many customers do we have?'")
    print("  • 'Show me our product information'")
    print("  • 'What are our sales numbers?'")
    print()
    
    print("💬 General Chat:")
    print("  • 'Hello Yara, how are you?'")
    print("  • 'Tell me a joke'")
    print("  • 'What\'s the weather like?'")
    print("  • 'Explain machine learning'")
    print()
    
    print("🔍 Intent Recognition:")
    print("  • 'Revenue' - Financial data queries")
    print("  • 'Customer' - Customer information")
    print("  • 'Product' - Product catalog")
    print("  • 'General' - Casual conversation")
    print()
    
    print("👋 Personal Questions:")
    print("  • 'Who are you?'")
    print("  • 'What can you do?'")
    print("  • 'Tell me about yourself'")
    print()

async def interactive_demo():
    """Run interactive demo with the chatbot."""
    try:
        # Import chatbot components
        from nlp import nlp_engine
        from db import db_manager
        
        print("🚀 Initializing Yara...")
        
        # Wait for model to load
        if not nlp_engine.model:
            print("⏳ Loading Yara's language model (this may take a moment)...")
            while not nlp_engine.model:
                await asyncio.sleep(1)
        
        print("✅ Yara is ready and excited to chat with you! ✨")
        print()
        
        # Show system status
        print("📊 Yara's System Status:")
        print(f"  • Model: {'✅ Loaded' if nlp_engine.model else '❌ Failed'}")
        print(f"  • Database: {'✅ Connected' if db_manager.is_connected else '❌ Not connected'}")
        if db_manager.is_connected:
            print(f"  • Database Type: {db_manager.engine.dialect.name}")
        print()
        
        # Show examples
        print_examples()
        
        # Start interactive loop
        conversation_history = []
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye! Thanks for trying the chatbot demo.")
                    break
                
                if user_input.lower() in ['help', 'examples']:
                    print_examples()
                    continue
                
                if user_input.lower() in ['status', 'info']:
                    print("📊 Yara's System Status:")
                    print(f"  • Model: {'✅ Loaded' if nlp_engine.model else '❌ Failed'}")
                    print(f"  • Database: {'✅ Connected' if db_manager.is_connected else '❌ Not connected'}")
                    if db_manager.is_connected:
                        print(f"  • Database Type: {db_manager.engine.dialect.name}")
                    print()
                    continue
                
                # Process the message
                print("🤖 Yara: ", end="", flush=True)
                
                start_time = time.time()
                
                # Get conversation context
                context = nlp_engine.get_context()
                
                # Generate response
                response = nlp_engine.generate_response(user_input, context)
                
                # Get intent information
                intent, confidence = nlp_engine.intent_recognizer.recognize_intent(user_input)
                
                # Add to conversation history
                nlp_engine.add_to_history(user_input, response)
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Display response
                print(response)
                print()
                
                # Show metadata
                print(f"📋 Intent: {intent} (confidence: {confidence:.2f})")
                print(f"⏱️  Response time: {response_time:.2f}s")
                
                # Show if database was used
                if db_manager.is_connected and intent in ['revenue_query', 'customer_query', 'product_query']:
                    print("🗄️  Database: Used for response")
                else:
                    print("🧠  Database: Not used (LLM response)")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for examples.")
                print()
    
    except ImportError as e:
        print(f"❌ Failed to import chatbot components: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def run_demo():
    """Run the demo."""
    print_header()
    
    try:
        asyncio.run(interactive_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user. Goodbye!")

if __name__ == "__main__":
    run_demo()
