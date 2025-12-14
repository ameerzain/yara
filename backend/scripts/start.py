#!/usr/bin/env python3
"""
Startup script for the chatbot system.
Provides easy access to different modes and testing.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def print_banner():
    """Print the chatbot banner."""
    print("""
🤖 Yara - Your Friendly AI Assistant
====================================
Meet Yara, your intelligent and friendly AI assistant who can help with 
conversations, answer questions, and provide organization insights!
""")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import transformers
        import torch
        import sqlalchemy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment configuration."""
    print("🔧 Checking environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Read and display key configs
        with open(env_file, 'r') as f:
            content = f.read()
            
        if 'DB_TYPE=' in content:
            db_type = [line for line in content.split('\n') if line.startswith('DB_TYPE=')][0]
            print(f"  Database: {db_type.split('=')[1]}")
        else:
            print("  Database: Not configured (general chat mode)")
            
        if 'MODEL_SIZE=' in content:
            model_size = [line for line in content.split('\n') if line.startswith('MODEL_SIZE=')][0]
            print(f"  Model Size: {model_size.split('=')[1]}")
        else:
            print("  Model Size: small (default)")
    else:
        print("⚠️  No .env file found")
        print("  Copy env.example to .env and configure your settings")
        print("  Running with default configuration")
    
    print()

def start_api_server(host="0.0.0.0", port=8000, debug=False):
    """Start the API server."""
    print(f"🚀 Starting API server on {host}:{port}")
    print(f"  Debug mode: {'Enabled' if debug else 'Disabled'}")
    print(f"  API docs: http://{host}:{port}/docs")
    print(f"  Health check: http://{host}:{port}/health")
    print()
    
    try:
        # Set environment variables
        env = os.environ.copy()
        if debug:
            env['DEBUG'] = 'True'
        
        # Start the server
        main_path = Path(__file__).parent.parent / 'src' / 'main.py'
        subprocess.run([
            sys.executable, str(main_path)
        ], env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def run_tests():
    """Run the test suite."""
    print("🧪 Running test suite...")
    
    try:
        test_path = Path(__file__).parent.parent / 'tests' / 'test_chatbot.py'
        subprocess.run([
            sys.executable, str(test_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_status():
    """Show system status."""
    print("📊 System Status")
    print("=" * 30)
    
    try:
        # Import and check components
        from config import AppConfig, ModelConfig
        from db import db_manager
        from nlp import nlp_engine
        
        print(f"Model Size: {ModelConfig.MODEL_SIZE}")
        print(f"Model Loaded: {'✅' if nlp_engine.model else '❌'}")
        print(f"Database Connected: {'✅' if db_manager.is_connected else '❌'}")
        if db_manager.is_connected:
            print(f"Database Type: {db_manager.engine.dialect.name}")
        print(f"API Host: {AppConfig.HOST}:{AppConfig.PORT}")
        print(f"Debug Mode: {'✅' if AppConfig.DEBUG else '❌'}")
        
    except Exception as e:
        print(f"❌ Could not determine status: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Intelligent Chatbot API Startup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start.py                    # Start with default settings
  python start.py --debug           # Start in debug mode
  python start.py --test            # Run tests only
  python start.py --status          # Show system status
  python start.py --host 127.0.0.1  # Start on specific host
        """
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Run test suite only'
    )
    
    parser.add_argument(
        '--status', 
        action='store_true',
        help='Show system status'
    )
    
    parser.add_argument(
        '--host', 
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port', 
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    check_environment()
    
    # Handle different modes
    if args.test:
        run_tests()
    elif args.status:
        show_status()
    else:
        # Start the API server
        start_api_server(
            host=args.host,
            port=args.port,
            debug=args.debug
        )

if __name__ == "__main__":
    main()
