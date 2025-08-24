# Yara - Your Friendly AI Assistant

Meet Yara, your intelligent and friendly AI assistant with state-of-the-art LLM capabilities and optional database integration! Built with FastAPI, Hugging Face Transformers, and SQLAlchemy, Yara is designed to be warm, helpful, and genuinely interested in assisting you.

## Features

### 🚀 **Dual Mode Operation**
- **General Chat Mode**: Uses open-source LLMs (DialoGPT) for natural, friendly conversations
- **Database Mode**: Integrates with MySQL/PostgreSQL for organization-specific data queries with enthusiasm

### 🧠 **Advanced NLP Capabilities**
- Intent recognition with pattern matching and semantic similarity
- Context-aware conversations with chat history
- Fallback responses for unknown queries
- Configurable model sizes (small/medium/large)
- **Yara's Personality**: Warm, enthusiastic, and genuinely helpful responses

### 🗄️ **Database Integration**
- Automatic database detection and connection
- Pre-built queries for revenue, customer, and product data
- Easy customization for different database schemas
- Support for both MySQL and PostgreSQL

### 🔧 **Production Ready**
- FastAPI backend with automatic API documentation
- CORS support for web integration
- Comprehensive logging and error handling
- Health checks and system monitoring
- Modular architecture for easy customization
- **Yara's Identity**: Personalized responses and friendly interaction patterns

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd chatbot-project

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
# For database mode, set DB_TYPE and database credentials
# For general chat only, leave DB_TYPE empty
```

### 3. Run the Server

```bash
# Start the API server
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **System Status**: http://localhost:8000/status
- **Meet Yara**: http://localhost:8000/ - Get to know your friendly AI assistant!

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_TYPE` | Database type: `mysql`, `postgresql`, or empty | None |
| `MODEL_SIZE` | LLM model size: `small`, `medium`, `large` | `small` |
| `HOST` | API server host | `0.0.0.0` |
| `PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `False` |

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

## API Usage

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What was our revenue last quarter?",
       "session_id": "user123"
     }'
```

**Response:**
```json
{
  "response": "Based on our last quarter data:\n• Total Revenue: $125,000.00\n• Number of Transactions: 1,250\n• Average Transaction: $100.00",
  "response": "Based on our last quarter data:\n• Total Revenue: $125,000.00\n• Number of Transactions: 1,250\n• Average Transaction: $100.00",
  "intent": "revenue_query",
  "confidence": 0.85,
  "session_id": "user123",
  "timestamp": 1703123456.789,
  "database_used": true
}
```

### System Status

```bash
curl "http://localhost:8000/status"
```

**Response:**
```json
{
  "status": "operational",
  "database_connected": true,
  "model_loaded": true,
  "uptime": 3600.5,
  "database_type": "mysql"
}
```

## Customization

### Adding New Intents

Edit `nlp.py` to add new intent patterns:

```python
self.intent_patterns = {
    'revenue_query': [...],
    'customer_query': [...],
    'product_query': [...],
    'general_chat': [...],
    'new_intent': [
        r'pattern1|pattern2',
        r'another_pattern'
    ]
}
```

### Custom Database Queries

Modify `db.py` to add new query methods:

```python
def get_custom_data(self, parameter: str) -> Optional[Dict]:
    """Custom query method."""
    query = "SELECT * FROM custom_table WHERE field = :param"
    return self.execute_query(query, {"param": parameter})
```

### Model Swapping

Change models in `config.py`:

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

## Project Structure

```
yara-assistant/
├── main.py              # FastAPI application entry point
├── routes.py            # API endpoint definitions
├── nlp.py              # NLP processing and LLM integration
├── db.py               # Database connection and queries
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── start.py            # Startup script with Yara's personality
├── demo.py             # Interactive demo with Yara
├── test_chatbot.py     # Test suite for Yara
└── README.md          # This file
```

## Yara's Personality & Capabilities

### 🌟 **What Makes Yara Special**
- **Friendly & Warm**: Always enthusiastic and genuinely interested in helping
- **Emoji Enthusiast**: Uses emojis to make conversations more engaging and fun
- **Context Aware**: Remembers conversation history for more natural interactions
- **Encouraging**: Provides positive reinforcement and celebrates user successes
- **Patient**: Takes time to explain things clearly and answer follow-up questions

### 💬 **Conversation Examples**
- **Greetings**: "Hi there! I'm Yara, and I'm so excited to meet you! 😊"
- **Database Queries**: "Great question! Here's what I found in our data: 📊"
- **Gratitude**: "You're very welcome! I'm so glad I could help! 😊"
- **Farewell**: "Goodbye! It was wonderful chatting with you! 👋✨"

## Database Schema

The system includes example table definitions for:
- **Transactions**: Revenue tracking
- **Customers**: Customer information
- **Products**: Product catalog

Customize these tables in `db.py` to match your organization's schema.

## Performance Considerations

### Model Selection
- **Small Model**: ~117M parameters, fast inference, lower quality
- **Medium Model**: ~345M parameters, balanced performance
- **Large Model**: ~774M parameters, slow inference, highest quality

### Database Optimization
- Use appropriate indexes on frequently queried fields
- Consider connection pooling for high-traffic scenarios
- Implement query caching for repeated requests

## Troubleshooting

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

### Logs

Check application logs for detailed error information:
```bash
# Logs are displayed in the console
# For production, configure proper logging to files
```

## Development

### Adding New Features

1. **New API Endpoints**: Add to `routes.py`
2. **New Intent Types**: Modify `nlp.py`
3. **New Database Queries**: Extend `db.py`
4. **Configuration Options**: Update `config.py`

### Testing

```bash
# Run with debug mode
DEBUG=True python main.py

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/status
```

## Production Deployment

### Environment Setup
```bash
# Production environment
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Process Management
```bash
# Using systemd
sudo systemctl enable chatbot
sudo systemctl start chatbot

# Using supervisor
supervisorctl start chatbot
```

### Reverse Proxy
```nginx
# Nginx configuration
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation at `/docs`
- Open an issue on GitHub

---

*Yara is excited to help you with anything you need! ✨🤖*

**Built with ❤️, your friendly AI assistant, using FastAPI, Hugging Face Transformers, and SQLAlchemy**