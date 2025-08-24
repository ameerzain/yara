"""
NLP/LLM processing module for the chatbot.
Handles model loading, intent recognition, and response generation.
"""
import logging
import re
from typing import Dict, List, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from config import ModelConfig, AppConfig
from db import db_manager
from memory import memory_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentRecognizer:
    """Recognizes user intent from input text."""
    
    def __init__(self):
        self.intent_patterns = {
            'revenue_query': [
                r'revenue|earnings|income|sales|money|profit|financial|quarter|year|month',
                r'how much|what was|total|amount|earned|made'
            ],
            'customer_query': [
                r'customer|client|user|buyer|purchaser',
                r'how many|count|list|show|find'
            ],
            'product_query': [
                r'product|item|goods|service|offering',
                r'price|cost|inventory|stock|available'
            ],
            'greeting': [
                r'hello|hi|hey|greeting|how are you|good morning|good afternoon|good evening',
                r'what\'s up|sup|yo|greetings'
            ],
            'personal_question': [
                r'who are you|what\'s your name|tell me about yourself|what can you do',
                r'your personality|your traits|about you'
            ],
            'gratitude': [
                r'thank you|thanks|thx|appreciate it|grateful|awesome|great|good job',
                r'well done|excellent|fantastic|amazing'
            ],
            'farewell': [
                r'goodbye|bye|see you|see ya|take care|farewell|until next time',
                r'have a good day|have a nice day|good night'
            ],
            'memory_query': [
                r'what is my \w+',
                r'what\'s my \w+',
                r'do you know my \w+',
                r'remember my \w+',
                r'where do i live',
                r'where am i from',
                r'what\'s my location'
            ],
            'memory_store': [
                r'my name is \w+',
                r'i\'m \w+',
                r'i am \w+',
                r'call me \w+',
                r'\w+ is my name',
                r'my favorite color is \w+',
                r'i like \w+',
                r'i love \w+',
                r'\w+ is my favorite color',
                r'i live in [^.!?]+',
                r'i\'m from [^.!?]+',
                r'my location is [^.!?]+',
                r'i\'m in [^.!?]+'
            ],
            'memory_manage': [
                r'forget my \w+',
                r'forget what i told you',
                r'remove my \w+',
                r'delete my \w+',
                r'clear my \w+',
                r'what do you remember',
                r'what do you know about me',
                r'show me what you remember',
                r'my information'
            ],
            'general_chat': [
                r'weather|joke|story|fun|entertainment|how\'s it going|what\'s new',
                r'chat|conversation|talk|discuss'
            ]
        }
        
        # Load sentence transformer for semantic similarity
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load sentence transformer: {e}")
            self.sentence_model = None
    
    def recognize_intent(self, text: str) -> Tuple[str, float]:
        """
        Recognize the intent of user input.
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (intent, confidence_score)
        """
        text_lower = text.lower()
        
        # Pattern-based intent recognition
        pattern_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 0.3  # Weight for pattern matching
            
            if score > 0:
                pattern_scores[intent] = score
        
        # Semantic similarity for better intent recognition
        if self.sentence_model:
            try:
                # Define intent examples
                intent_examples = {
                    'revenue_query': [
                        'What was our revenue last quarter?',
                        'How much money did we make?',
                        'What are our earnings?'
                    ],
                    'customer_query': [
                        'How many customers do we have?',
                        'Show me customer information',
                        'List our clients'
                    ],
                    'product_query': [
                        'What products do we offer?',
                        'Show me our inventory',
                        'What are our prices?'
                    ],
                    'greeting': [
                        'Hello, how are you?',
                        'Hi there!',
                        'Good morning!',
                        'Hey, what\'s up?'
                    ],
                    'personal_question': [
                        'Who are you?',
                        'What\'s your name?',
                        'Tell me about yourself',
                        'What can you do?'
                    ],
                    'gratitude': [
                        'Thank you!',
                        'Thanks a lot',
                        'I appreciate it',
                        'Great job!'
                    ],
                    'farewell': [
                        'Goodbye!',
                        'See you later',
                        'Take care',
                        'Have a good day!'
                    ],
                    'memory_query': [
                        'What is my name?',
                        'What\'s my favorite color?',
                        'Where do I live?',
                        'Do you know my name?'
                    ],
                    'memory_store': [
                        'My name is Alex',
                        'I like blue',
                        'I live in New York',
                        'Call me John'
                    ],
                    'memory_manage': [
                        'Forget my name',
                        'What do you remember?',
                        'Clear my information'
                    ],
                    'general_chat': [
                        'Tell me a joke',
                        'What\'s the weather like?',
                        'How\'s it going?',
                        'What\'s new?'
                    ]
                }
                
                # Calculate semantic similarity
                text_embedding = self.sentence_model.encode([text])
                
                for intent, examples in intent_examples.items():
                    example_embeddings = self.sentence_model.encode(examples)
                    similarities = cosine_similarity(text_embedding, example_embeddings)[0]
                    semantic_score = np.max(similarities) * 0.7  # Weight for semantic similarity
                    
                    if intent in pattern_scores:
                        pattern_scores[intent] += semantic_score
                    else:
                        pattern_scores[intent] = semantic_score
                        
            except Exception as e:
                logger.warning(f"Semantic similarity failed: {e}")
        
        # Determine best intent
        if pattern_scores:
            best_intent = max(pattern_scores.items(), key=lambda x: x[1])
            confidence = min(best_intent[1], 1.0)  # Cap confidence at 1.0
            
            if confidence >= AppConfig.INTENT_THRESHOLD:
                return best_intent[0], confidence
        
        # Default to general chat if no clear intent
        return 'general_chat', 0.5

class ChatbotNLP:
    """Main NLP processing class for the chatbot."""
    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.intent_recognizer = IntentRecognizer()
        self.chat_history = []
        self._load_model()
    
    def _load_model(self):
        """Load the configured LLM model."""
        try:
            model_config = ModelConfig.get_model_config()
            model_name = model_config['name']
            
            logger.info(f"Loading model: {model_name}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=model_config['max_length'],
                temperature=model_config['temperature'],
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            logger.info(f"Model {model_name} loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None
            self.generator = None
    
    def generate_response(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Generate a response based on user input and context.
        
        Args:
            user_input: User's message
            context: Optional context information
            
        Returns:
            Generated response string
        """
        # First, check if this is a memory-related operation
        memory_response, memory_action = memory_manager.process_input(user_input)
        if memory_response:
            logger.info(f"Memory operation detected: {memory_action}")
            return memory_response
        
        # Recognize intent
        intent, confidence = self.intent_recognizer.recognize_intent(user_input)
        logger.info(f"Recognized intent: {intent} (confidence: {confidence:.2f})")
        
        # Handle database queries if database is available
        if db_manager.is_connected and intent in ['revenue_query', 'customer_query', 'product_query']:
            db_response = self._handle_database_query(intent, user_input)
            if db_response:
                return db_response
        
        # Check if confidence is too low - use fallback immediately
        if confidence < AppConfig.INTENT_THRESHOLD:
            logger.info(f"Low confidence ({confidence:.2f}) < threshold ({AppConfig.INTENT_THRESHOLD}), using fallback")
            return self._get_fallback_response(intent, user_input)
        
        # Check if we should force fallback for this intent
        forced_fallback = self._force_fallback_for_intent(intent, user_input)
        if forced_fallback:
            logger.info(f"Using forced fallback for intent: {intent}")
            return forced_fallback
        
        # Generate general response using LLM
        if self.generator:
            try:
                # Prepare input with context, memory context, and Yara's personality
                personality_instruction = "You are Yara, a friendly, enthusiastic, and helpful AI assistant. Always be warm, encouraging, and use emojis to make conversations enjoyable. Be genuinely interested in helping users and show enthusiasm for their questions."
                
                # Get memory context
                memory_context = memory_manager.get_context_for_nlp()
                
                # Build full input
                input_parts = []
                if context:
                    input_parts.append(f"Context: {context}")
                if memory_context:
                    input_parts.append(f"Memory: {memory_context}")
                input_parts.append(personality_instruction)
                input_parts.append(f"User: {user_input}")
                input_parts.append("Yara:")
                
                full_input = "\n".join(input_parts)
                
                # Generate response
                response = self.generator(
                    full_input,
                    max_length=len(full_input.split()) + 50,
                    num_return_sequences=1
                )
                
                if response and len(response) > 0:
                    generated_text = response[0]['generated_text']
                    # Extract only Yara's response
                    if "Yara:" in generated_text:
                        yara_response = generated_text.split("Yara:")[-1].strip()
                    else:
                        # Fallback to Assistant: if Yara: is not found
                        yara_response = generated_text.split("Assistant:")[-1].strip()
                    
                    # Validate the generated response quality
                    if self._is_valid_response(yara_response, user_input, intent):
                        return yara_response
                    else:
                        logger.info("Generated response failed quality check, using fallback")
                        return self._get_fallback_response(intent, user_input)
                    
            except Exception as e:
                logger.error(f"Model generation failed: {e}")
        
        # Fallback responses
        return self._get_fallback_response(intent, user_input)
    
    def _force_fallback_for_intent(self, intent: str, user_input: str) -> str:
        """
        Force fallback response for specific intents that should never use LLM generation.
        
        Args:
            intent: Recognized intent
            user_input: User's message
            
        Returns:
            Appropriate fallback response
        """
        # Force fallback for personal questions to ensure consistent responses
        if intent == 'personal_question':
            return self._get_fallback_response(intent, user_input)
        
        # Force fallback for greetings to ensure consistent personality
        if intent == 'greeting':
            return self._get_fallback_response(intent, user_input)
        
        # Force fallback for gratitude and farewell
        if intent in ['gratitude', 'farewell']:
            return self._get_fallback_response(intent, user_input)
        
        # Force fallback for memory operations (handled by memory manager)
        if intent in ['memory_query', 'memory_store', 'memory_manage']:
            return self._get_fallback_response(intent, user_input)
        
        # Force fallback for database queries when no database is available
        if not db_manager.is_connected and intent in ['revenue_query', 'customer_query', 'product_query']:
            return self._get_fallback_response(intent, user_input)
        
        # Allow LLM generation for other intents
        return None
    
    def _is_valid_response(self, response: str, user_input: str, intent: str) -> bool:
        """
        Validate if the generated response is appropriate and relevant.
        
        Args:
            response: Generated response to validate
            user_input: Original user input
            intent: Recognized intent
            
        Returns:
            True if response is valid, False otherwise
        """
        if not AppConfig.ENABLE_RESPONSE_VALIDATION:
            return True
            
        if not response or len(response.strip()) < AppConfig.MIN_RESPONSE_LENGTH:
            return False
        
        # Check for inappropriate or nonsensical responses
        inappropriate_phrases = [
            'waifu', 'hero that\'s needed', 'who is this', 'tell me about your',
            'i am the', 'i am a', 'i am', 'i\'m the', 'i\'m a'
        ]
        
        response_lower = response.lower()
        for phrase in inappropriate_phrases:
            if phrase in response_lower:
                return False
        
        # Check if response is too generic or doesn't address the intent
        if intent == 'personal_question' and 'who are you' in user_input.lower():
            # For personal questions, ensure response is about Yara
            personal_keywords = ['yara', 'assistant', 'ai', 'help', 'friendly', 'helpful']
            if not any(keyword in response_lower for keyword in personal_keywords):
                return False
        
        # Check response length (not too short, not too long)
        if len(response.strip()) > AppConfig.MAX_RESPONSE_LENGTH:
            return False
        
        return True
    
    def _handle_database_query(self, intent: str, user_input: str) -> Optional[str]:
        """
        Handle database-specific queries.
        
        Args:
            intent: Recognized intent
            user_input: User's message
            
        Returns:
            Formatted response string or None if query fails
        """
        try:
            if intent == 'revenue_query':
                # Extract time period from user input
                if 'quarter' in user_input.lower():
                    period = 'last_quarter'
                elif 'year' in user_input.lower():
                    period = 'last_year'
                elif 'month' in user_input.lower():
                    period = 'current_month'
                else:
                    period = 'last_quarter'  # Default
                
                revenue_data = db_manager.get_revenue_data(period)
                if revenue_data:
                    return self._format_revenue_response(revenue_data, period)
            
            elif intent == 'customer_query':
                customer_data = db_manager.get_customer_data()
                if customer_data:
                    return self._format_customer_response(customer_data)
            
            elif intent == 'product_query':
                product_data = db_manager.get_product_data()
                if product_data:
                    return self._format_product_response(product_data)
                    
        except Exception as e:
            logger.error(f"Database query failed: {e}")
        
        return None
    
    def _format_revenue_response(self, data: Dict, period: str) -> str:
        """Format revenue data into a readable response."""
        period_names = {
            'last_quarter': 'last quarter',
            'last_year': 'last year',
            'current_month': 'this month'
        }
        
        period_name = period_names.get(period, period)
        total = data.get('total_revenue', 0)
        count = data.get('transaction_count', 0)
        avg = data.get('average_transaction', 0)
        
        return f"Great question! Here's what I found in our {period_name} data: 📊\n\n" \
               f"• **Total Revenue**: ${total:,.2f} 💰\n" \
               f"• **Number of Transactions**: {count:,} 📈\n" \
               f"• **Average Transaction**: ${avg:.2f} 📊\n\n" \
               f"I hope this information is helpful! Is there anything specific about these numbers you'd like me to explain? 😊"
    
    def _format_customer_response(self, data: List[Dict]) -> str:
        """Format customer data into a readable response."""
        total_customers = len(data)
        return f"Awesome! I'm happy to share that we currently have **{total_customers:,} wonderful customers** in our database! 🎉\n\n" \
               f"That's quite a community we're building! Is there anything specific about our customers you'd like to know more about? 😊"
    
    def _format_product_response(self, data: List[Dict]) -> str:
        """Format product data into a readable response."""
        total_products = len(data)
        categories = set(item.get('category', 'Unknown') for item in data)
        return f"Fantastic! I'm excited to tell you about our product offerings! 🛍️\n\n" \
               f"We currently offer **{total_products:,} amazing products** across **{len(categories)} different categories**! 📦\n\n" \
               f"That's quite a diverse selection! Would you like me to tell you more about any specific category or product? 😊"
    
    def _get_fallback_response(self, intent: str, user_input: str) -> str:
        """Get fallback responses when model generation fails."""
        fallback_responses = {
            'revenue_query': "I'm sorry, I couldn't retrieve the revenue information at the moment. Please try again later or contact our support team.",
            'customer_query': "I'm unable to access customer data right now. Please check back later or reach out to our team for assistance.",
            'product_query': "I'm having trouble accessing product information. Please try again later or contact our support team.",
            'greeting': "Hi there! I'm Yara, and I'm so excited to meet you! 😊 How can I help you today?",
            'personal_question': "I'm Yara, your friendly AI assistant! I'm here to help with conversations, answer questions, and provide insights from your data. I love being helpful and making our chats enjoyable! ✨",
            'gratitude': "You're very welcome! I'm so glad I could help! 😊 It makes me happy when I can be useful to you.",
            'farewell': "Goodbye! It was wonderful chatting with you! Take care and come back anytime - I'll be here ready to help! 👋✨",
            'memory_query': "I'm not sure I understood that question. Could you rephrase it or ask me something else? 🤔",
            'memory_store': "I'm not sure I understood that. Could you rephrase it or ask me something else? 🤔",
            'memory_manage': "I'm not sure I understood that request. Could you rephrase it or ask me something else? 🤔",
            'general_chat': "I'm not sure I understood that, could you rephrase? 🤔"
        }
        
        # Enhanced fallback responses with more context
        enhanced_fallbacks = {
            'personal_question': {
                'who are you': "I'm Yara, your friendly AI assistant! I'm here to help with conversations, answer questions, and provide insights from your data. I love being helpful and making our chats enjoyable! ✨",
                'what\'s your name': "My name is Yara! I'm your friendly AI assistant, and I'm excited to help you with whatever you need! 😊",
                'tell me about yourself': "I'm Yara, a friendly and enthusiastic AI assistant! I love helping people, answering questions, and making conversations enjoyable. I'm here to assist you with both general chat and data insights! ✨",
                'what can you do': "I can help you with conversations, answer questions, provide insights from your data, and be a friendly chat companion! I'm Yara, and I'm excited to assist you! 😊"
            }
        }
        
        # Check for enhanced fallbacks first
        if intent in enhanced_fallbacks:
            for pattern, response in enhanced_fallbacks[intent].items():
                if pattern in user_input.lower():
                    return response
        
        return fallback_responses.get(intent, fallback_responses['general_chat'])
    
    def add_to_history(self, user_input: str, response: str):
        """Add conversation to chat history."""
        self.chat_history.append({
            'user': user_input,
            'assistant': response,
            'timestamp': None  # Could add timestamp if needed
        })
        
        # Limit history length
        if len(self.chat_history) > AppConfig.MAX_HISTORY_LENGTH:
            self.chat_history.pop(0)
    
    def get_context(self) -> str:
        """Get recent conversation context for better responses."""
        if not self.chat_history:
            return ""
        
        # Get last few exchanges for context
        recent_exchanges = self.chat_history[-3:]
        context_parts = []
        
        for exchange in recent_exchanges:
            context_parts.append(f"User: {exchange['user']}")
            context_parts.append(f"Yara: {exchange['assistant']}")
        
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Clear chat history."""
        self.chat_history.clear()
        # Also reset session memory when clearing history
        memory_manager.reset_session()

# Global NLP instance
nlp_engine = ChatbotNLP()
