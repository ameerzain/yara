#!/usr/bin/env python3
"""
Launcher script for Yara backend and optionally the frontend UI.
This script sets up the Python path and runs the main application.

Usage:
    python main.py              # Start backend only
    python main.py --ui         # Start both backend and UI
    python main.py --help      # Show help message
"""
import sys
import argparse
import subprocess
import time
import webbrowser
from pathlib import Path

# Add backend/src to Python path
backend_src = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_src))

def start_backend():
    """Start the backend API server."""
    import uvicorn
    from config import AppConfig
    from main import app
    
    print("🚀 Starting Yara Backend API...")
    print(f"📍 API will be available at http://{AppConfig.HOST}:{AppConfig.PORT}")
    print(f"📚 API docs: http://{AppConfig.HOST}:{AppConfig.PORT}/docs")
    print()
    
    uvicorn.run(
        app,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=AppConfig.DEBUG,
        log_level="info"
    )

def start_ui(port=8001):
    """Start the frontend UI server in a separate process."""
    frontend_dir = Path(__file__).parent / 'frontend'
    start_ui_script = frontend_dir / 'start_ui.py'
    
    if not start_ui_script.exists():
        print("⚠️  Frontend UI files not found. Starting backend only.")
        return None
    
    try:
        print(f"🌐 Starting Frontend UI on port {port}...")
        ui_process = subprocess.Popen(
            [sys.executable, str(start_ui_script), str(port)],
            cwd=str(frontend_dir)
        )
        
        # Wait a moment for UI server to start
        time.sleep(2)
        
        if ui_process.poll() is None:
            print(f"✅ Frontend UI started at http://localhost:{port}")
            print()
            return ui_process
        else:
            print("⚠️  Frontend UI failed to start. Continuing with backend only.")
            return None
    except Exception as e:
        print(f"⚠️  Could not start frontend UI: {e}")
        print("   Continuing with backend only...")
        return None

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Start Yara - Your Friendly AI Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Start backend API only
  python main.py --ui         # Start both backend and frontend UI
  python main.py --ui --port 8002  # Start UI on custom port
        """
    )
    
    parser.add_argument(
        '--ui',
        action='store_true',
        help='Also start the frontend UI server'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8001,
        help='Port for frontend UI server (default: 8001)'
    )
    
    args = parser.parse_args()
    
    if args.ui:
        print("=" * 60)
        print("🎯 Starting Yara - Complete System")
        print("=" * 60)
        print()
        
        # Start UI in background
        ui_process = start_ui(args.port)
        
        if ui_process:
            print("💡 Both servers are running:")
            print(f"   • Backend API: http://localhost:8000")
            print(f"   • Frontend UI: http://localhost:{args.port}")
            print()
            print("Press Ctrl+C to stop both servers")
            print("=" * 60)
            print()
        
        # Start backend (this will block)
        try:
            start_backend()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            if ui_process:
                ui_process.terminate()
                print("✅ Frontend UI stopped")
    else:
        print("=" * 60)
        print("🎯 Starting Yara - Backend API Only")
        print("=" * 60)
        print()
        print("💡 To also start the frontend UI, use: python main.py --ui")
        print()
        print("=" * 60)
        print()
        start_backend()

if __name__ == "__main__":
    main()

