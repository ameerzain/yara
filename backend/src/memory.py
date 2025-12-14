"""
Session memory module for the chatbot.
Handles storing and retrieving user information during chat sessions.
"""
import logging
import re
from typing import Dict, Optional, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class SessionMemory:
    """Manages session-based memory for user information."""
    
    def __init__(self):
        self.memory: Dict[str, any] = {}
        self.memory_metadata: Dict[str, Dict] = {}  # Track when/how info was stored
        self.session_start = datetime.now()
        
    def store(self, key: str, value: str, source: str = "user_input") -> None:
        """
        Store information in session memory.
        
        Args:
            key: Memory key (e.g., 'name', 'favorite_color')
            value: Information to store
            source: How the information was obtained ('user_input', 'extracted', etc.)
        """
        self.memory[key] = value
        self.memory_metadata[key] = {
            'timestamp': datetime.now(),
            'source': source,
            'session_age': (datetime.now() - self.session_start).total_seconds()
        }
        logger.info(f"Stored in memory: {key} = {value}")
    
    def retrieve(self, key: str) -> Optional[str]:
        """
        Retrieve information from session memory.
        
        Args:
            key: Memory key to retrieve
            
        Returns:
            Stored value or None if not found
        """
        return self.memory.get(key)
    
    def has_key(self, key: str) -> bool:
        """Check if a key exists in memory."""
        return key in self.memory
    
    def remove(self, key: str) -> bool:
        """
        Remove information from memory.
        
        Args:
            key: Memory key to remove
            
        Returns:
            True if key was found and removed, False otherwise
        """
        if key in self.memory:
            del self.memory[key]
            del self.memory_metadata[key]
            logger.info(f"Removed from memory: {key}")
            return True
        return False
    
    def clear(self) -> None:
        """Clear all session memory."""
        self.memory.clear()
        self.memory_metadata.clear()
        self.session_start = datetime.now()
        logger.info("Session memory cleared")
    
    def get_all(self) -> Dict[str, any]:
        """Get all stored memory as a dictionary."""
        return self.memory.copy()
    
    def get_memory_summary(self) -> str:
        """Get a human-readable summary of stored memory."""
        if not self.memory:
            return "I don't have any information stored yet."
        
        summary_parts = []
        for key, value in self.memory.items():
            summary_parts.append(f"• {key}: {value}")
        
        return "Here's what I remember:\n" + "\n".join(summary_parts)

class MemoryManager:
    """High-level memory management with natural language understanding."""
    
    def __init__(self):
        self.session_memory = SessionMemory()
        
        # Patterns for recognizing memory-related queries
        self.memory_patterns = {
            'store_name': [
                r'^my name is (\w+)$',
                r'^i\'m (\w+)$',
                r'^i am (\w+)$',
                r'^call me (\w+)$',
                r'^(\w+) is my name$'
            ],
            'store_favorite_color': [
                r'^my favorite color is (\w+)$',
                r'^my fav color is (\w+)$',
                r'^my fav clr is (\w+)$',
                r'^i like (\w+)$',
                r'^i love (\w+)$',
                r'^(\w+) is my favorite color$'
            ],
            'store_location': [
                r'^i live in ([^.!?]+)$',
                r'^i\'m from ([^.!?]+)$',
                r'^my location is ([^.!?]+)$',
                r'^i\'m in ([^.!?]+)$'
            ],
            'query_name': [
                r'^what is my name\??$',
                r'^what\'s my name\??$',
                r'^do you know my name\??$',
                r'^remember my name\??$',
                r'^my name\??$'
            ],
            'query_favorite_color': [
                r'^what is my favorite color\??$',
                r'^what is my fav color\??$',
                r'^what is my fav clr\??$',
                r'^what\'s my favorite color\??$',
                r'^do you know my favorite color\??$',
                r'^my favorite color\??$'
            ],
            'query_location': [
                r'^where do i live\??$',
                r'^where am i from\??$',
                r'^what\'s my location\??$',
                r'^my location\??$'
            ],
            'forget_request': [
                r'forget my (\w+)',
                r'forget what i told you',
                r'remove my (\w+)',
                r'delete my (\w+)',
                r'clear my (\w+)'
            ],
            'memory_summary': [
                r'what do you remember\??',
                r'what do you know about me\??',
                r'show me what you remember\??',
                r'my information\??'
            ]
        }
    
    def process_input(self, user_input: str) -> Tuple[Optional[str], str]:
        """
        Process user input for memory operations.
        
        Args:
            user_input: User's message
            
        Returns:
            Tuple of (response_message, memory_action)
            memory_action can be: 'store', 'query', 'forget', 'summary', 'none'
        """
        user_input_lower = user_input.lower()
        
        # Check for forget patterns FIRST (highest priority)
        for pattern in self.memory_patterns['forget_request']:
            match = re.search(pattern, user_input_lower)
            if match:
                if 'what i told you' in user_input_lower:
                    self.session_memory.clear()
                    return "Alright, I'll forget everything you told me for now. 🧹", 'forget'
                else:
                    extracted_key = match.group(1)
                    # Try to find the actual key in memory
                    actual_key = None
                    for key in self.session_memory.memory.keys():
                        if extracted_key in key or key in extracted_key:
                            actual_key = key
                            break
                    
                    if actual_key:
                        self.session_memory.remove(actual_key)
                        return f"Alright, I'll forget your {actual_key} for now. 🧹", 'forget'
                    else:
                        return f"I don't have your {extracted_key} stored, so there's nothing to forget. 🤷‍♀️", 'forget'
        
        # Check for memory summary (high priority)
        for pattern in self.memory_patterns['memory_summary']:
            if re.search(pattern, user_input_lower):
                return self.session_memory.get_memory_summary(), 'summary'
        
        # Check for store patterns
        for pattern_type, patterns in self.memory_patterns.items():
            if pattern_type.startswith('store_'):
                for pattern in patterns:
                    match = re.search(pattern, user_input_lower)
                    if match:
                        key = pattern_type.replace('store_', '')
                        value = match.group(1).strip()
                        self.session_memory.store(key, value)
                        
                        if key == 'name':
                            return f"Nice to meet you, {value}! I'll remember that during this chat. 😊", 'store'
                        elif key == 'favorite_color':
                            return f"Got it! I'll remember that your favorite color is {value}. 🎨", 'store'
                        elif key == 'location':
                            return f"Thanks! I'll remember you're from {value}. 🌍", 'store'
                        else:
                            return f"I'll remember that your {key} is {value}. 👍", 'store'
        
        # Check for query patterns LAST (lowest priority)
        for pattern_type, patterns in self.memory_patterns.items():
            if pattern_type.startswith('query_'):
                for pattern in patterns:
                    if re.search(pattern, user_input_lower):
                        key = pattern_type.replace('query_', '')
                        stored_value = self.session_memory.retrieve(key)
                        
                        if stored_value:
                            if key == 'name':
                                return f"Your name is {stored_value}. 😊", 'query'
                            elif key == 'favorite_color':
                                return f"Your favorite color is {stored_value}. 🎨", 'query'
                            elif key == 'location':
                                return f"You're from {stored_value}. 🌍", 'query'
                            else:
                                return f"Your {key} is {stored_value}. 👍", 'query'
                        else:
                            if key == 'name':
                                return "I don't know yet! What's your name? 😊", 'query'
                            elif key == 'favorite_color':
                                return "I don't know yet! What's your favorite color? 🎨", 'query'
                            elif key == 'location':
                                return "I don't know yet! Where are you from? 🌍", 'query'
                            else:
                                return f"I don't know your {key} yet. Could you tell me? 🤔", 'query'
        
        # No memory operation detected
        return None, 'none'
    
    def get_context_for_nlp(self) -> str:
        """
        Get memory context formatted for NLP processing.
        
        Returns:
            Formatted string with memory context
        """
        if not self.session_memory.memory:
            return ""
        
        context_parts = ["User Information:"]
        for key, value in self.session_memory.memory.items():
            context_parts.append(f"- {key}: {value}")
        
        return "\n".join(context_parts)
    
    def reset_session(self) -> None:
        """Reset the current session memory."""
        self.session_memory.clear()

# Global memory manager instance
memory_manager = MemoryManager()
