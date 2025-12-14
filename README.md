# Yara - Your Friendly AI Assistant 🤖✨

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Meet **Yara**, an intelligent and friendly AI assistant with state-of-the-art LLM capabilities and optional database integration. Built with FastAPI, Hugging Face Transformers, and SQLAlchemy, Yara is designed to be warm, helpful, and genuinely interested in assisting you.

## 🌟 Features

### 🚀 Dual Mode Operation
- **General Chat Mode**: Uses open-source LLMs (DialoGPT) for natural, friendly conversations
- **Database Mode**: Integrates with MySQL/PostgreSQL for organization-specific data queries

### 🧠 Advanced NLP Capabilities
- Intent recognition with pattern matching and semantic similarity
- Context-aware conversations with chat history
- Session-based memory system for personalized interactions
- Fallback responses for unknown queries
- Configurable model sizes (small/medium/large)
- **Yara's Personality**: Warm, enthusiastic, and genuinely helpful responses

### 🗄️ Database Integration
- Automatic database detection and connection
- Pre-built queries for revenue, customer, and product data
- Easy customization for different database schemas
- Support for both MySQL and PostgreSQL

### 🎨 Web Interface
- Modern, responsive chat UI
- Real-time messaging
- Session management
- Customizable settings

### 🔧 Production Ready
- FastAPI backend with automatic API documentation
- CORS support for web integration (configurable)
- Comprehensive logging and error handling
- Global exception handler for graceful error recovery
- Health checks and system monitoring
- Response validation and automatic fallback system
- Modular architecture for easy customization

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Customization](#-customization)
- [Development](#-development)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) MySQL or PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ameerzain/yara.git
   cd yara
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run the server**
   ```bash
   # Start backend only (easiest way)
   python main.py
   
   # Start both backend AND frontend UI together
   python main.py --ui
   
   # Or start them separately:
   # Terminal 1: Backend
   python main.py
   # Terminal 2: Frontend
   python frontend/start_ui.py
   
   # Alternative: Use module approach
   python -m backend.src.main
   
   # Or use the startup script
   python backend/scripts/start.py
   ```

6. **Access the application**
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **Frontend UI**: http://localhost:8001 (if started with `--ui` flag)

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_TYPE` | Database type: `mysql`, `postgresql`, or empty | None |
| `MODEL_SIZE` | LLM model size: `small`, `medium`, `large` | `small` |
| `HOST` | API server host | `0.0.0.0` |
| `PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `False` |
| `INTENT_THRESHOLD` | Confidence threshold for intent recognition | `0.7` |
| `MAX_HISTORY_LENGTH` | Maximum conversation history length | `10` |
| `RESPONSE_TIMEOUT` | Maximum time (seconds) to wait for response | `30` |
| `MIN_RESPONSE_LENGTH` | Minimum response length for quality validation | `10` |
| `MAX_RESPONSE_LENGTH` | Maximum response length for quality validation | `500` |
| `ENABLE_RESPONSE_VALIDATION` | Enable/disable response quality validation | `True` |
| `FALLBACK_ON_LOW_QUALITY` | Enable/disable fallback for low-quality responses | `True` |

### Database Configuration

#### MySQL
```env
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=chatbot_db
```

#### PostgreSQL
```env
DB_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=chatbot_db
```

**Note**: Leave `DB_TYPE` empty to run in general chat mode only (no database required).

#### How Database Connection Works

The system automatically detects and connects to the database on startup:

1. **Connection Initialization**: When the server starts, `DatabaseManager` (in `backend/src/db.py`) reads the `DB_TYPE` from your `.env` file
2. **Connection Test**: If `DB_TYPE` is set, it attempts to connect and runs a test query (`SELECT 1`)
3. **Status Tracking**: Connection status is stored in `db_manager.is_connected` (boolean flag)
4. **Automatic Fallback**: If connection fails, the system logs an error but continues running in general chat mode
5. **Status Endpoint**: Check connection status via `/status` endpoint which returns `database_connected: true/false`

**Connection Status Check**:
- The code checks `db_manager.is_connected` before executing any database queries
- If not connected, database-dependent intents (revenue_query, customer_query, product_query) will use fallback responses
- You can verify connection status in the API response: `"database_used": true/false`

## 💻 Usage

### Running the Server

```bash
# Basic startup (easiest)
python main.py

# Or as a module
python -m backend.src.main

# Or using the startup script with options
python backend/scripts/start.py --debug          # Enable debug mode
python backend/scripts/start.py --host 127.0.0.1     # Custom host
python backend/scripts/start.py --port 8080         # Custom port
python backend/scripts/start.py --status            # Show system status
```


### Web UI

**Option 1: Start both together (Recommended)**
```bash
python main.py --ui
```
This starts both the backend API (port 8000) and frontend UI (port 8001) automatically.

**Option 2: Start separately**
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Start frontend
python frontend/start_ui.py
```

**Option 3: Open HTML directly**
1. Start backend: `python main.py`
2. Open `frontend/index.html` directly in your browser

The web UI provides:
- Modern, responsive chat interface
- Real-time messaging with Yara
- **API Status Monitoring**: Automatic connection detection with retry logic
- **Session Management**: Persistent session IDs for conversation tracking
- **Settings Modal**: Customize API endpoint, session ID, and other preferences
- **Character Counter**: Track message length with visual feedback
- **Auto-resize Textarea**: Dynamic input field that grows with content
- **Error Handling**: User-friendly error toasts for connection issues
- **Auto-scroll**: Automatic scrolling to latest messages
- **Conversation History**: View and clear chat history

### API Usage

#### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What was our revenue last quarter?",
       "session_id": "user123",
       "context": "Optional context information"
     }'
```

**Request Parameters:**
- `message` (required): Your message to Yara (1-1000 characters)
- `session_id` (optional): Session ID for conversation tracking
- `context` (optional): Additional context information for the conversation

**Response:**
```json
{
  "response": "Great question! Here's what I found in our last quarter data: 📊\n\n• Total Revenue: $125,000.00 💰\n• Number of Transactions: 1,250 📈\n• Average Transaction: $100.00 📊",
  "intent": "revenue_query",
  "confidence": 0.85,
  "session_id": "user123",
  "timestamp": 1703123456.789,
  "database_used": true,
  "assistant_name": "Yara"
}
```

#### System Status

```bash
curl "http://localhost:8000/status"
```

**Response:**
```json
{
  "status": "operational",
  "assistant_name": "Yara",
  "database_connected": true,
  "model_loaded": true,
  "uptime": 1234.56,
  "database_type": "mysql"
}
```

#### Clear Chat History

```bash
# Clear all history
curl -X DELETE "http://localhost:8000/chat/history"

# Clear specific session history
curl -X DELETE "http://localhost:8000/chat/history?session_id=user123"
```

#### Database Information

```bash
curl "http://localhost:8000/database/info"
```

**Response (when connected):**
```json
{
  "connected": true,
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "chatbot_db",
  "username": "root",
  "tables": ["transactions", "customers", "products"]
}
```

## 📚 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API information |
| `/chat` | POST | Chat with Yara |
| `/status` | GET | Get system status |
| `/health` | GET | Health check endpoint |
| `/chat/history` | DELETE | Clear chat history |
| `/database/info` | GET | Get database information |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation (ReDoc) |

### Request/Response Models

See the interactive API documentation at `/docs` for detailed request/response schemas.

## 📁 Project Structure

```
yara/
├── backend/                # Backend Python code
│   ├── src/                # Source code
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── routes.py       # API endpoint definitions
│   │   ├── nlp.py         # NLP processing and LLM integration
│   │   ├── db.py          # Database connection and queries
│   │   ├── memory.py      # Session memory management
│   │   └── config.py      # Configuration management
│   ├── scripts/           # Utility scripts
│   │   └── start.py       # Startup script with options
│   ├── tests/             # Test suite
│   │   └── test_chatbot.py
│   └── requirements.txt   # Python dependencies
├── frontend/              # Frontend web interface
│   ├── index.html         # Main HTML file
│   ├── chatbot.js         # Chatbot JavaScript logic
│   ├── config.js          # UI configuration
│   ├── styles.css         # Styling
│   └── start_ui.py        # UI launcher
├── docs/                  # Additional documentation
│   ├── ARCHITECTURE_EXPLAINED.md  # How frontend/backend work
│   └── ARCHITECTURE.md            # Technical implementation details
├── env.example            # Environment variables template
├── CONTRIBUTING.md        # Contributing guidelines
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🎨 Customization

### Adding New Intents

Edit `backend/src/nlp.py` to add new intent patterns:

```python
self.intent_patterns = {
    'revenue_query': [...],
    'customer_query': [...],
    'product_query': [...],
    'new_intent': [
        r'pattern1|pattern2',
        r'another_pattern'
    ]
}
```

### Custom Database Queries

Modify `backend/src/db.py` to add new query methods:

```python
def get_custom_data(self, parameter: str) -> Optional[Dict]:
    """Custom query method."""
    query = "SELECT * FROM custom_table WHERE field = :param"
    return self.execute_query(query, {"param": parameter})
```

### Model Configuration

Change models in `backend/src/config.py`:

```python
MODELS = {
    'small': {
        'name': 'microsoft/DialoGPT-small',
        'max_length': 512,
        'temperature': 0.7
    },
    'custom': {
        'name': 'your-custom-model',
        'max_length': 1024,
        'temperature': 0.8
    }
}
```

### Session Memory

The memory system allows Yara to remember user information during chat sessions:

**Storage Examples:**
- "My name is Alex" → Stores name in session memory
- "My favorite color is blue" → Stores favorite color
- "I live in New York" → Stores location

**Query Examples:**
- "What is my name?" → Returns stored name
- "What is my favorite color?" → Returns stored color
- "Where do I live?" → Returns stored location

**Memory Management:**
- "Forget my favorite color" → Removes specific information
- "Forget what I told you" → Clears all stored information
- "What do you remember?" → Shows all stored information

**Supported Memory Types:**
- Name, favorite color, location, and custom information
- Memory persists during the session
- Memory is cleared when session ends or explicitly cleared

## 🧪 Development

### Running Tests

```bash
python backend/tests/test_chatbot.py
```

### Development Mode

```bash
DEBUG=True python -m backend.src.main
```

### Code Structure

- **Modular Design**: Each component (NLP, database, memory) is separated for easy maintenance
- **Type Hints**: Code includes type hints for better IDE support
- **Logging**: Comprehensive logging throughout the application
- **Error Handling**: Robust error handling with fallback mechanisms
- **Global Exception Handler**: Catches and handles unhandled exceptions gracefully
- **CORS Support**: Configured for cross-origin requests (customize for production)

### Response Validation & Fallback System

Yara includes a sophisticated response validation and fallback system:

**Response Quality Validation:**
- Validates response length (MIN_RESPONSE_LENGTH to MAX_RESPONSE_LENGTH)
- Checks for meaningful content (not just whitespace or errors)
- Can be enabled/disabled via `ENABLE_RESPONSE_VALIDATION`

**Automatic Fallback:**
- If response quality is low, automatically uses fallback responses
- Fallback responses are context-aware and intent-specific
- Can be enabled/disabled via `FALLBACK_ON_LOW_QUALITY`

**Fallback Triggers:**
- Response too short or too long
- Empty or invalid responses
- Model generation failures
- Database query failures (for database-dependent intents)
- **Global Exception Handler**: Catches and handles unhandled exceptions gracefully
- **CORS Support**: Configured for cross-origin requests (customize for production)

### Response Validation & Fallback System

Yara includes a sophisticated response validation and fallback system:

**Response Quality Validation:**
- Validates response length (MIN_RESPONSE_LENGTH to MAX_RESPONSE_LENGTH)
- Checks for meaningful content (not just whitespace or errors)
- Can be enabled/disabled via `ENABLE_RESPONSE_VALIDATION`

**Automatic Fallback:**
- If response quality is low, automatically uses fallback responses
- Fallback responses are context-aware and intent-specific
- Can be enabled/disabled via `FALLBACK_ON_LOW_QUALITY`

**Fallback Triggers:**
- Response too short or too long
- Empty or invalid responses
- Model generation failures
- Database query failures (for database-dependent intents)

## 📚 Documentation

For more detailed information, see the following documentation:

- **[Architecture Explained](docs/ARCHITECTURE_EXPLAINED.md)** - Detailed explanation of how frontend and backend work together, what each component does, and how data flows through the system
- **[Technical Architecture](docs/ARCHITECTURE.md)** - Deep dive into the fallback system, memory management, response validation, and implementation details
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project, code style, testing, and submission process

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

Quick steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to new functions
- Include docstrings for new modules and functions
- Update tests for new features
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Fails**
   - Check available memory (models require 2-8GB RAM)
   - Verify internet connection for model download
   - Try smaller model size

2. **Database Connection Fails**
   - Verify database credentials in `.env`
   - Ensure database server is running
   - Check firewall settings

3. **Slow Response Times**
   - Use smaller model size
   - Enable GPU acceleration if available
   - Optimize database queries

4. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+)

## 📊 Performance Considerations

### Model Selection

- **Small Model**: ~117M parameters, fast inference, lower quality
- **Medium Model**: ~345M parameters, balanced performance
- **Large Model**: ~774M parameters, slow inference, highest quality

### Database Optimization

- Use appropriate indexes on frequently queried fields
- Consider connection pooling for high-traffic scenarios
- Implement query caching for repeated requests

## 🔒 Security

- Never commit `.env` files with real credentials
- Use environment variables for sensitive information
- Configure CORS appropriately for production
- Keep dependencies up to date

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Hugging Face Transformers](https://huggingface.co/transformers/) - Pre-trained models
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit
- [DialoGPT](https://huggingface.co/microsoft/DialoGPT-medium) - Conversation model

## 📞 Support

For issues and questions:
- Check the [Troubleshooting](#-troubleshooting) section
- Review the API documentation at `/docs`
- Read the [Architecture Documentation](docs/ARCHITECTURE_EXPLAINED.md) for understanding how components work
- Open an issue on GitHub

---

## 📖 Additional Resources

- **[Architecture Explained](docs/ARCHITECTURE_EXPLAINED.md)** - Learn how frontend and backend components work together
- **[Technical Details](docs/ARCHITECTURE.md)** - Implementation details, fallback system, and memory management
- **[Contributing](CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[License](LICENSE)** - MIT License

---

**Built with ❤️ using FastAPI, Hugging Face Transformers, and SQLAlchemy**

*Yara is excited to help you with anything you need! ✨🤖*
