#!/usr/bin/env python3
"""
Simple startup script for the Yara Chatbot UI
Starts a local HTTP server to serve the chatbot interface
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_server(port=8001):
    """Start a local HTTP server for the chatbot UI."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the UI directory
    os.chdir(script_dir)
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"=== Starting Yara Chatbot UI server...")
            print(f"=== Serving files from: {script_dir}")
            print(f"=== Server running at: http://localhost:{port}")
            print(f"=== Chatbot UI: http://localhost:{port}/index.html")
            print()
            print("=== Make sure your Yara backend is running at http://localhost:8000")
            print("=== Open the above URL in your browser to test the chatbot")
            print()
            print("Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f"http://localhost:{port}/index.html")
                print("=== Browser opened automatically!")
            except:
                print("===  Please open your browser manually")
            
            # Start serving
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"=== Port {port} is already in use!")
            print(f"💡 Try a different port: python start-ui.py {port + 1}")
        else:
            print(f"=== Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n=== Server stopped by user")
        sys.exit(0)

def main():
    """Main entry point."""
    # Parse command line arguments
    port = 8001
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("=== Invalid port number. Using default port 8001")
            port = 8001
    
    # Check if required files exist
    required_files = ['index.html', 'styles.css', 'config.js', 'chatbot.js']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print("=== Missing required files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\n💡 Make sure you're running this script from the chatbot-ui directory")
        sys.exit(1)
    
    # Start the server
    start_server(port)

if __name__ == "__main__":
    main()
