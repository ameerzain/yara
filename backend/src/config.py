"""
Configuration file for the chatbot system.
Contains database connection settings and model configurations.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration settings."""
    
    # Database type: 'mysql', 'postgresql', or None for no database
    DB_TYPE = os.getenv('DB_TYPE', None)
    
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'chatbot_db')
    
    # PostgreSQL Configuration
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'chatbot_db')
    
    @classmethod
    def get_connection_string(cls) -> Optional[str]:
        """Get database connection string based on configuration."""
        if cls.DB_TYPE == 'mysql':
            return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}"
        elif cls.DB_TYPE == 'postgresql':
            return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}"
        return None

class ModelConfig:
    """LLM model configuration settings."""
    
    # Model selection: 'small', 'medium', 'large'
    MODEL_SIZE = os.getenv('MODEL_SIZE', 'small')
    
    # Model configurations for different sizes
    MODELS = {
        'small': {
            'name': 'microsoft/DialoGPT-small',
            'max_length': 512,
            'temperature': 0.7
        },
        'medium': {
            'name': 'microsoft/DialoGPT-medium',
            'max_length': 1024,
            'temperature': 0.7
        },
        'large': {
            'name': 'microsoft/DialoGPT-large',
            'max_length': 2048,
            'temperature': 0.7
        }
    }
    
    @classmethod
    def get_model_config(cls):
        """Get current model configuration."""
        return cls.MODELS.get(cls.MODEL_SIZE, cls.MODELS['small'])

class AppConfig:
    """Application configuration settings."""
    
    # API Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Chat Configuration
    MAX_HISTORY_LENGTH = int(os.getenv('MAX_HISTORY_LENGTH', 10))
    RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 30))
    
    # Intent Recognition
    INTENT_THRESHOLD = float(os.getenv('INTENT_THRESHOLD', 0.7))
    
    # Response Quality & Fallback
    MIN_RESPONSE_LENGTH = int(os.getenv('MIN_RESPONSE_LENGTH', 10))
    MAX_RESPONSE_LENGTH = int(os.getenv('MAX_RESPONSE_LENGTH', 500))
    ENABLE_RESPONSE_VALIDATION = os.getenv('ENABLE_RESPONSE_VALIDATION', 'True').lower() == 'true'
    FALLBACK_ON_LOW_QUALITY = os.getenv('FALLBACK_ON_LOW_QUALITY', 'True').lower() == 'true'
