# 🤖 Yara Chatbot UI

A modern, responsive web-based chatbot interface for testing your Yara backend API. Built with vanilla HTML, CSS, and JavaScript for easy customization and deployment.

## ✨ Features

- **Modern Design**: Clean, professional chat interface with smooth animations
- **Real-time Chat**: Send messages and receive responses from your Yara API
- **Conversation History**: Scrollable chat history with message timestamps
- **Session Management**: Automatic session ID generation and management
- **Settings Panel**: Configure API endpoint, session ID, and UI preferences
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Error Handling**: Graceful error handling with user-friendly notifications
- **Auto-scroll**: Automatic scrolling to new messages (configurable)
- **Character Count**: Real-time character counting with visual feedback
- **API Status**: Live API connection status indicator

## 🚀 Quick Start

### 1. Setup

1. **Copy the UI files** to your web server or local development environment
2. **Ensure your Yara backend** is running (default: `http://localhost:8000`)
3. **Open `index.html`** in your web browser

### 2. Configuration

The UI will automatically:
- Connect to `http://localhost:8000/chat` by default
- Generate a unique session ID for each chat session
- Test the API connection on startup

### 3. Customization

- **API Endpoint**: Change the API URL in Settings
- **Styling**: Modify `styles.css` to match your brand
- **Functionality**: Extend `chatbot.js` for additional features

## 📁 File Structure

```
chatbot-ui/
├── index.html          # Main HTML file
├── styles.css          # CSS styling and animations
├── config.js           # Configuration management
├── chatbot.js          # Main chatbot functionality
└── README.md           # This file
```

## ⚙️ Configuration Options

### API Settings
- **API Endpoint**: URL of your Yara backend `/chat` endpoint
- **Session ID**: Custom session identifier (optional)
- **Max History**: Maximum number of messages to keep in memory (10-100)
- **Auto-scroll**: Automatically scroll to new messages

### Default Configuration
```javascript
{
    apiUrl: 'http://localhost:8000/chat',
    sessionId: null, // Auto-generated
    maxHistory: 50,
    autoScroll: true,
    maxMessageLength: 1000
}
```

## 🎨 Customization

### Changing Colors
Modify the CSS variables in `styles.css`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --error-color: #ef4444;
}
```

### Adding New Features
Extend the `ChatbotApp` class in `chatbot.js`:

```javascript
class ChatbotApp {
    // ... existing code ...
    
    // Add new method
    newFeature() {
        // Your custom functionality
    }
}
```

### Styling Modifications
- **Message Bubbles**: Modify `.message-text` styles
- **Header Design**: Update `.chat-header` styles
- **Input Area**: Customize `.chat-input-area` styles
- **Animations**: Adjust keyframe animations

## 🔧 API Integration

### Expected API Response Format
Your Yara backend should return responses in this format:

```json
{
    "response": "Hello! I'm Yara, how can I help you?",
    "intent": "greeting",
    "confidence": 0.95,
    "session_id": "session_123",
    "timestamp": 1703123456.789,
    "database_used": false,
    "assistant_name": "Yara"
}
```

### Required Fields
- `response`: The chatbot's response text
- `intent`: Recognized intent (optional)
- `confidence`: Confidence score (optional)

### Optional Fields
- `session_id`: Session identifier
- `timestamp`: Response timestamp
- `database_used`: Whether database was used
- `assistant_name`: Name of the AI assistant

## 📱 Responsive Design

The UI automatically adapts to different screen sizes:

- **Desktop**: Full-width layout with optimal spacing
- **Tablet**: Adjusted spacing and touch-friendly elements
- **Mobile**: Compact layout with mobile-optimized interactions

## 🚀 Deployment

### Local Development
```bash
# Start a local server (Python 3)
python -m http.server 8001

# Or use Node.js
npx http-server -p 8001

# Then open http://localhost:8001
```

### Production Deployment
1. **Upload files** to your web server
2. **Update API endpoint** in settings to your production URL
3. **Configure CORS** on your backend if needed
4. **Test thoroughly** before going live

### CORS Configuration
If you encounter CORS issues, ensure your Yara backend allows requests from your UI domain:

```python
# In your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing

### Manual Testing
1. **Send messages** and verify responses
2. **Test error scenarios** (disconnect API, invalid responses)
3. **Check responsive design** on different screen sizes
4. **Verify settings persistence** across browser sessions

### Automated Testing
The UI is built with testable code structure:

```javascript
// Access chatbot instance for testing
const chatbot = window.chatbot;

// Test methods
chatbot.sendMessage();
chatbot.clearChat();
chatbot.testApiConnection();
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Verify your backend is running
   - Check the API endpoint URL in settings
   - Ensure CORS is properly configured

2. **Messages Not Sending**
   - Check browser console for errors
   - Verify API endpoint is accessible
   - Check network tab for failed requests

3. **Styling Issues**
   - Clear browser cache
   - Verify CSS file is loaded
   - Check for JavaScript errors

4. **Mobile Issues**
   - Test on different mobile devices
   - Verify viewport meta tag
   - Check touch event handling

### Debug Mode
Enable debug logging in the browser console:

```javascript
// In browser console
localStorage.setItem('chatbotDebug', 'true');
location.reload();
```

## 🎯 Browser Support

- **Chrome**: 80+ ✅
- **Firefox**: 75+ ✅
- **Safari**: 13+ ✅
- **Edge**: 80+ ✅
- **Mobile Browsers**: iOS Safari 13+, Chrome Mobile ✅

## 📈 Performance

- **Lightweight**: No heavy frameworks or dependencies
- **Fast Loading**: Optimized CSS and JavaScript
- **Efficient Rendering**: Minimal DOM manipulation
- **Memory Management**: Automatic message history cleanup

## 🔒 Security Features

- **Input Sanitization**: XSS prevention for user messages
- **CORS Handling**: Proper cross-origin request handling
- **Error Boundaries**: Graceful error handling without exposing internals
- **Session Isolation**: Separate session IDs for different users

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review browser console for errors
- Test with different browsers
- Verify API endpoint accessibility

---

**Built with ❤️ for Yara - Your Friendly AI Assistant! ✨🤖**
