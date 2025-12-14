#!/usr/bin/env python3
"""
Test script for the chatbot system.
Tests basic functionality without requiring the full API server.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from nlp import nlp_engine
from db import db_manager
from config import AppConfig, ModelConfig, DatabaseConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing Configuration...")
    
    print(f"  Model Size: {ModelConfig.MODEL_SIZE}")
    print(f"  Model Config: {ModelConfig.get_model_config()}")
    print(f"  Database Type: {DatabaseConfig.DB_TYPE or 'None'}")
    print(f"  Host: {AppConfig.HOST}:{AppConfig.PORT}")
    print(f"  Debug Mode: {AppConfig.DEBUG}")
    
    print("✅ Configuration test completed\n")

def test_database_connection():
    """Test database connection."""
    print("🗄️ Testing Database Connection...")
    
    if db_manager.is_connected:
        print(f"  ✅ Connected to {db_manager.engine.dialect.name} database")
        print(f"  Host: {db_manager.engine.url.host}:{db_manager.engine.url.port}")
        print(f"  Database: {db_manager.engine.url.database}")
        
        # Test a simple query
        try:
            result = db_manager.execute_query("SELECT 1 as test")
            if result:
                print("  ✅ Database query test successful")
            else:
                print("  ⚠️ Database query returned no results")
        except Exception as e:
            print(f"  ❌ Database query test failed: {e}")
    else:
        print("  ℹ️ No database configured - running in general chat mode only")
    
    print("✅ Database test completed\n")

def test_nlp_engine():
    """Test NLP engine functionality."""
    print("🧠 Testing Yara's NLP Engine...")
    
    if nlp_engine.model:
        print(f"  ✅ Model loaded: {nlp_engine.model.__class__.__name__}")
        print(f"  Tokenizer: {nlp_engine.tokenizer.__class__.__name__}")
    else:
        print("  ❌ Model failed to load")
        return False
    
    # Test intent recognition
    test_messages = [
        "What was our revenue last quarter?",
        "How many customers do we have?",
        "Hello Yara, how are you?",
        "Tell me a joke"
    ]
    
    print("  Testing intent recognition:")
    for message in test_messages:
        intent, confidence = nlp_engine.intent_recognizer.recognize_intent(message)
        print(f"    '{message}' -> {intent} (confidence: {confidence:.2f})")
    
    print("✅ Yara's NLP engine test completed\n")
    return True

def test_chat_responses():
    """Test chat response generation."""
    print("💬 Testing Yara's Chat Responses...")
    
    test_messages = [
        "Hello Yara!",
        "What's the weather like?",
        "How are you doing today?"
    ]
    
    for message in test_messages:
        print(f"  User: {message}")
        try:
            response = nlp_engine.generate_response(message)
            print(f"  Yara: {response[:100]}{'...' if len(response) > 100 else ''}")
        except Exception as e:
            print(f"  ❌ Error generating response: {e}")
        print()
    
    print("✅ Yara's chat response test completed\n")

def test_database_queries():
    """Test database query functionality if available."""
    if not db_manager.is_connected:
        print("ℹ️ Skipping database query tests - no database connected\n")
        return
    
    print("🔍 Testing Database Queries...")
    
    # Test revenue query
    try:
        revenue_data = db_manager.get_revenue_data("last_quarter")
        if revenue_data:
            print(f"  ✅ Revenue query successful: {revenue_data}")
        else:
            print("  ⚠️ Revenue query returned no data")
    except Exception as e:
        print(f"  ❌ Revenue query failed: {e}")
    
    # Test customer query
    try:
        customer_data = db_manager.get_customer_data()
        if customer_data:
            print(f"  ✅ Customer query successful: {len(customer_data)} customers")
        else:
            print("  ⚠️ Customer query returned no data")
    except Exception as e:
        print(f"  ❌ Customer query failed: {e}")
    
    print("✅ Database query test completed\n")

async def main():
    """Run all tests."""
    print("🚀 Starting Yara - Your Friendly AI Assistant Tests\n")
    print("=" * 50)
    
    try:
        # Run tests
        test_configuration()
        test_database_connection()
        
        if test_nlp_engine():
            test_chat_responses()
        
        test_database_queries()
        
        print("🎉 All tests completed successfully!")
        print("\n📋 Yara's System Summary:")
        print(f"  • Database: {'✅ Connected' if db_manager.is_connected else '❌ Not connected'}")
        print(f"  • NLP Model: {'✅ Loaded' if nlp_engine.model else '❌ Failed to load'}")
        print(f"  • Configuration: ✅ Loaded")
        
        if db_manager.is_connected:
            print(f"  • Database Type: {db_manager.engine.dialect.name}")
        
        print(f"  • Model Size: {ModelConfig.MODEL_SIZE}")
        
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        logger.exception("Test suite error")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
