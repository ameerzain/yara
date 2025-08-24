"""
Main entry point for the chatbot API.
Sets up FastAPI application and registers all routes.
"""
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from config import AppConfig, ModelConfig, DatabaseConfig
from routes import (
    chat_endpoint_func,
    status_endpoint_func,
    health_endpoint_func,
    clear_history_endpoint_func,
    database_info_endpoint_func
)
from routes import ChatRequest, ChatResponse, SystemStatus, HealthCheck

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global startup/shutdown events
@asynccontextmanager
async def lifespan(main: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting Yara - Your Friendly AI Assistant...")
    logger.info("✨ Yara is ready to help with conversations and insights!")
    logger.info(
        f"Configuration: Model size={ModelConfig.MODEL_SIZE}, Database={DatabaseConfig.DB_TYPE or 'None'}"
    )
    
    yield
    
    # Shutdown
    logger.info("🛑 Yara is shutting down... Goodbye for now!")
    # Clean up resources if needed

# Create FastAPI application
app = FastAPI(
    title="Yara - Your Friendly AI Assistant",
    description="Meet Yara, your intelligent and friendly AI assistant who can help with conversations, answer questions, and provide organization insights through database integration.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# API Routes
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat with Yara, your friendly AI assistant!
    
    - **message**: Your message to Yara (required)
    - **session_id**: Optional session ID for conversation tracking
    - **context**: Optional context information
    
    Yara will respond with helpful, friendly assistance and insights.
    """
    return await chat_endpoint_func(request)

@app.get("/status", response_model=SystemStatus, tags=["System"])
async def get_status():
    """
    Get system status and health information.
    
    Returns current system status including database connection,
    model loading status, and uptime information.
    """
    return await status_endpoint_func()

@app.get("/health", response_model=HealthCheck, tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns basic health status and API version information.
    """
    return await health_endpoint_func()

@app.delete("/chat/history", tags=["Chat"])
async def clear_history(session_id: str = None):
    """
    Clear chat history.
    
    - **session_id**: Optional session ID to clear specific session history
    
    Clears all chat history if no session ID is provided.
    """
    return await clear_history_endpoint_func(session_id)

@app.get("/database/info", tags=["Database"])
async def get_database_info():
    """
    Get database connection information and available tables.
    
    Returns database connection status, type, and available tables
    if a database is configured and connected.
    """
    return await database_info_endpoint_func()

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns basic information about Yara, your friendly AI assistant.
    """
    return {
        "message": "Hello! I'm Yara, your friendly AI assistant! 🤖✨",
        "version": "1.0.0",
        "description": "I'm here to help you with conversations, answer questions, and provide insights from your organization's data. I'm friendly, helpful, and always ready to assist!",
        "personality": {
            "name": "Yara",
            "traits": ["Friendly", "Helpful", "Intelligent", "Patient", "Enthusiastic"],
            "greeting": "Hi there! I'm Yara, and I'm excited to help you today! 😊"
        },
        "endpoints": {
            "chat": "/chat - Chat with Yara",
            "status": "/status - System status",
            "health": "/health - Health check",
            "database": "/database/info - Database information",
            "docs": "/docs - API documentation"
        },
        "quick_start": "Send a message to /chat to start chatting with me!"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Yara - Your Friendly AI Assistant...")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=AppConfig.DEBUG,
        log_level="info"
    )
