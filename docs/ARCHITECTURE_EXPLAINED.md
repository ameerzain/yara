# Yara Architecture Explained

This document explains what each part of the Yara project does and how they work together.

## 🎯 Overview

Yara has two main parts:
1. **Backend (Python/FastAPI)** - The "brain" that processes messages and generates responses
2. **Frontend (chatbot-ui/)** - The "face" that users interact with in their browser

---

## 📁 chatbot-ui/ Folder (Frontend - What Users See)

The `chatbot-ui/` folder contains a **web-based chat interface** that users interact with in their browser.

### What It Does:
- Provides a visual chat interface (like a messaging app)
- Sends user messages to the backend API
- Displays responses from Yara
- Manages conversation history
- Handles UI interactions (typing indicators, settings, etc.)

### Files in chatbot-ui/:

#### `index.html`
- **Purpose**: The main HTML page that users see
- **Contains**: 
  - Chat message area
  - Input box for typing messages
  - Header with Yara's name and settings
  - Modal dialogs for settings
- **Think of it as**: The structure/skeleton of the chat interface

#### `styles.css`
- **Purpose**: Makes the interface look beautiful
- **Contains**: 
  - Colors, fonts, spacing
  - Animations (typing indicators, message fade-ins)
  - Responsive design (works on mobile/tablet/desktop)
- **Think of it as**: The styling/makeup of the interface

#### `chatbot.js`
- **Purpose**: The "brain" of the frontend
- **Contains**:
  - Sends messages to backend API (`/chat` endpoint)
  - Receives and displays responses
  - Manages conversation history
  - Handles user interactions (send button, clear chat, settings)
  - Shows typing indicators
  - Error handling
- **Think of it as**: The JavaScript logic that makes everything work

#### `config.js`
- **Purpose**: Configuration and utility functions
- **Contains**:
  - Default API URL (`http://localhost:8000/chat`)
  - Session ID management
  - Settings storage (localStorage)
  - Helper functions (timestamp formatting, input sanitization)
- **Think of it as**: Settings and helper utilities

#### `start_ui.py`
- **Purpose**: Simple Python script to run a local web server
- **What it does**: 
  - Starts a local HTTP server (port 8001)
  - Serves the HTML/CSS/JS files
  - Opens browser automatically
- **Why needed**: Browsers need a web server to load files (security reasons)

### How chatbot-ui Works:

```
User types message
    ↓
chatbot.js sends POST request to http://localhost:8000/chat
    ↓
Backend processes message and returns response
    ↓
chatbot.js receives response and displays it in the chat
```

---

## 🐍 Main Project Files (Backend - The Brain)

These files are in the `org_chatbot/` folder (outside of `chatbot-ui/`).

### What They Do:
- Process user messages using AI/LLM
- Connect to databases (if configured)
- Generate intelligent responses
- Manage conversation context and memory
- Provide REST API endpoints

### Key Files:

#### `main.py`
- **Purpose**: The entry point - starts the FastAPI server
- **What it does**:
  - Creates the FastAPI application
  - Registers all API routes
  - Sets up CORS (allows frontend to connect)
  - Handles startup/shutdown
  - Runs on port 8000
- **Think of it as**: The main server that listens for requests

#### `routes.py`
- **Purpose**: Defines all API endpoints
- **Endpoints**:
  - `POST /chat` - Main chat endpoint (receives messages, returns responses)
  - `GET /status` - System status (database connected? model loaded?)
  - `GET /health` - Health check
  - `DELETE /chat/history` - Clear conversation history
  - `GET /database/info` - Database information
- **Think of it as**: The API contract - what endpoints are available

#### `nlp.py` (Natural Language Processing)
- **Purpose**: The "intelligence" - understands and generates responses
- **What it does**:
  - **Intent Recognition**: Understands what the user wants (greeting, question, database query, etc.)
  - **LLM Integration**: Uses DialoGPT models to generate conversational responses
  - **Response Generation**: Creates Yara's responses
  - **Quality Control**: Validates responses and uses fallbacks if needed
  - **Context Management**: Remembers conversation history
- **Think of it as**: Yara's brain - understands language and generates smart responses

#### `db.py` (Database)
- **Purpose**: Connects to and queries databases
- **What it does**:
  - Connects to MySQL or PostgreSQL (if configured)
  - Executes queries for revenue, customers, products
  - Returns formatted data
- **Think of it as**: Yara's memory for business data (optional - can run without database)

#### `memory.py` (Session Memory)
- **Purpose**: Remembers user information during chat sessions
- **What it does**:
  - Stores user info (name, favorite color, location, etc.)
  - Understands memory-related requests ("What's my name?", "Forget my favorite color")
  - Provides context to NLP for personalized responses
- **Think of it as**: Yara's short-term memory for the current conversation

#### `config.py`
- **Purpose**: Manages all configuration settings
- **What it does**:
  - Reads environment variables (`.env` file)
  - Provides database connection settings
  - Manages model configuration (small/medium/large)
  - Application settings (host, port, debug mode)
- **Think of it as**: Settings manager - everything configurable

#### `start.py`
- **Purpose**: Convenient startup script with options
- **What it does**:
  - Checks dependencies
  - Validates configuration
  - Starts the server with various options
  - Can run tests or show status
- **Think of it as**: A helper script to start Yara easily

#### `test_chatbot.py`
- **Purpose**: Automated tests
- **What it does**:
  - Tests all components
  - Verifies everything works correctly
- **Think of it as**: Quality assurance

---

## 🔄 How Everything Works Together

### Complete Flow:

```
1. User opens chatbot-ui/index.html in browser
   ↓
2. chatbot.js loads and connects to http://localhost:8000
   ↓
3. User types: "What was our revenue last quarter?"
   ↓
4. chatbot.js sends POST request to /chat endpoint
   ↓
5. routes.py receives request and calls nlp.py
   ↓
6. nlp.py:
   - Recognizes intent: "revenue_query"
   - Checks if database is connected (db.py)
   - If yes: queries database for revenue data
   - If no: generates general response
   ↓
7. nlp.py formats response with Yara's personality
   ↓
8. routes.py returns JSON response to chatbot.js
   ↓
9. chatbot.js displays response in the chat interface
```

### Two Ways to Use Yara:

#### Option 1: Web Interface (chatbot-ui/)
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Start UI server
cd chatbot-ui
python start_ui.py

# Open browser to http://localhost:8001
```

#### Option 2: API (Command Line)
```bash
# Start backend
python main.py

# Use curl or any HTTP client to chat
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello Yara!"}'
```

---

## 🎨 Separation of Concerns

### Frontend (chatbot-ui/)
- **Responsibility**: User interface and interaction
- **Technology**: HTML, CSS, JavaScript
- **Does NOT**: Process AI, connect to databases
- **Only**: Sends requests and displays responses

### Backend (main files)
- **Responsibility**: AI processing, database, business logic
- **Technology**: Python, FastAPI, Transformers
- **Does NOT**: Handle UI rendering or browser interactions
- **Only**: Processes requests and returns data

### Why This Separation?
- **Flexibility**: Can use different frontends (web, mobile app, CLI)
- **Scalability**: Backend can handle multiple frontends
- **Maintainability**: Clear boundaries between UI and logic
- **Testing**: Can test backend independently

---

## 📊 Data Flow Example

### Example: User asks "What's my name?"

```
User Input: "What's my name?"
    ↓
[Frontend] chatbot.js sends to /chat
    ↓
[Backend] routes.py receives request
    ↓
[Backend] nlp.py processes:
    - Checks memory.py: "Do I know user's name?"
    - If yes: Returns "Your name is Alex"
    - If no: Returns "I don't know yet! What's your name?"
    ↓
[Backend] routes.py returns JSON response
    ↓
[Frontend] chatbot.js receives response
    ↓
[Frontend] Displays in chat: "Your name is Alex"
```

---

## 🔧 Configuration Files

### `env.example` / `.env`
- **Purpose**: Environment variables for configuration
- **Contains**: Database credentials, model settings, API settings
- **Used by**: `config.py` reads these values

### `requirements.txt`
- **Purpose**: Python package dependencies
- **Contains**: All libraries needed (FastAPI, transformers, etc.)
- **Used by**: `pip install -r requirements.txt`

---

## 🎯 Summary

| Component | Location | Purpose | Technology |
|-----------|----------|---------|------------|
| **Web UI** | `chatbot-ui/` | User interface | HTML/CSS/JS |
| **API Server** | `main.py` | Receives requests | FastAPI |
| **Endpoints** | `routes.py` | API definitions | FastAPI |
| **AI Brain** | `nlp.py` | Understands & responds | Transformers |
| **Database** | `db.py` | Data queries | SQLAlchemy |
| **Memory** | `memory.py` | Remembers user info | Python dicts |
| **Config** | `config.py` | Settings | Python |

**In Simple Terms:**
- **chatbot-ui/** = The pretty face users see
- **Main files** = The smart brain that thinks and responds

Both work together to create the complete Yara experience! ✨

