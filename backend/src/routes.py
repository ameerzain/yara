"""
API routes for the chatbot system.
Defines FastAPI endpoints for chat functionality and system management.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import time

try:
    from .nlp import nlp_engine
    from .db import db_manager
    from .config import AppConfig
except ImportError:
    from nlp import nlp_engine
    from db import db_manager
    from config import AppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message", min_length=1, max_length=1000)
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")
    context: Optional[str] = Field(None, description="Optional context information")

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Yara's friendly response")
    intent: str = Field(..., description="Recognized intent")
    confidence: float = Field(..., description="Confidence score for intent recognition")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")
    timestamp: float = Field(..., description="Response timestamp")
    database_used: bool = Field(..., description="Whether database was used for response")
    assistant_name: str = Field(default="Yara", description="Name of the AI assistant")

class SystemStatus(BaseModel):
    """System status response model."""
    status: str = Field(..., description="System status")
    assistant_name: str = Field(default="Yara", description="Name of the AI assistant")
    database_connected: bool = Field(..., description="Database connection status")
    model_loaded: bool = Field(..., description="LLM model loading status")
    uptime: float = Field(..., description="System uptime in seconds")
    database_type: Optional[str] = Field(None, description="Type of database connected")

class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    assistant_name: str = Field(default="Yara", description="Name of the AI assistant")
    timestamp: float = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")

# Global variables
start_time = time.time()
api_version = "1.0.0"

def get_system_status() -> SystemStatus:
    """Get current system status."""
    current_time = time.time()
    uptime = current_time - start_time
    
    return SystemStatus(
        status="operational",
        assistant_name="Yara",
        database_connected=db_manager.is_connected,
        model_loaded=nlp_engine.model is not None,
        uptime=uptime,
        database_type=db_manager.engine.dialect.name if db_manager.engine else None
    )

def get_health_status() -> HealthCheck:
    """Get system health status."""
    return HealthCheck(
        status="healthy",
        assistant_name="Yara",
        timestamp=time.time(),
        version=api_version
    )

# API endpoints
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for processing user messages.
    
    Args:
        request: Chat request containing user message and optional context
        
    Returns:
        ChatResponse with chatbot's response and metadata
    """
    try:
        start_time = time.time()
        
        # Get conversation context if available
        context = None
        if request.session_id:
            context = nlp_engine.get_context()
        
        # Generate response
        response = nlp_engine.generate_response(request.message, context)
        
        # Get intent information
        intent, confidence = nlp_engine.intent_recognizer.recognize_intent(request.message)
        
        # Add to conversation history
        nlp_engine.add_to_history(request.message, response)
        
        # Determine if database was used
        database_used = (
            db_manager.is_connected and 
            intent in ['revenue_query', 'customer_query', 'product_query']
        )
        
        # Log the interaction
        processing_time = time.time() - start_time
        logger.info(f"Yara processed chat in {processing_time:.2f}s - Intent: {intent} (confidence: {confidence:.2f})")
        
        return ChatResponse(
            response=response,
            intent=intent,
            confidence=confidence,
            session_id=request.session_id,
            timestamp=time.time(),
            database_used=database_used,
            assistant_name="Yara"
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during chat processing")

async def status_endpoint() -> SystemStatus:
    """Get system status and health information."""
    return get_system_status()

async def health_endpoint() -> HealthCheck:
    """Health check endpoint for monitoring."""
    return get_health_status()

async def clear_history_endpoint(session_id: Optional[str] = None) -> Dict[str, str]:
    """Clear chat history for a specific session or all sessions."""
    try:
        if session_id:
            # In a real implementation, you might want to clear specific session history
            # For now, we'll clear all history
            pass
        
        nlp_engine.clear_history()
        return {"message": "Chat history cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

async def database_info_endpoint() -> Dict[str, Any]:
    """Get database connection information and available tables."""
    try:
        if not db_manager.is_connected:
            return {
                "connected": False,
                "message": "No database configured or connection failed"
            }
        
        # Get database info
        db_info = {
            "connected": True,
            "type": db_manager.engine.dialect.name,
            "host": db_manager.engine.url.host,
            "port": db_manager.engine.url.port,
            "database": db_manager.engine.url.database,
            "username": db_manager.engine.url.username
        }
        
        # Try to get table information
        try:
            with db_manager.engine.connect() as conn:
                # Get table names (this is a simplified approach)
                if db_manager.engine.dialect.name == 'mysql':
                    result = conn.execute(db_manager.engine.text("SHOW TABLES"))
                elif db_manager.engine.dialect.name == 'postgresql':
                    result = conn.execute(db_manager.engine.text(
                        "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
                    ))
                else:
                    result = None
                
                if result:
                    tables = [row[0] for row in result.fetchall()]
                    db_info["tables"] = tables
                    
        except Exception as e:
            logger.warning(f"Could not retrieve table information: {e}")
            db_info["tables"] = []
        
        return db_info
        
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve database information")

# Export the endpoints for use in main.py
chat_endpoint_func = chat_endpoint
status_endpoint_func = status_endpoint
health_endpoint_func = health_endpoint
clear_history_endpoint_func = clear_history_endpoint
database_info_endpoint_func = database_info_endpoint
