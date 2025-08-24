/**
 * Main Chatbot Application
 * Handles chat functionality, API communication, and UI interactions
 */

class ChatbotApp {
    constructor() {
        this.config = new ChatbotConfig.ConfigManager();
        this.sessionId = this.config.get('sessionId') || ChatbotConfig.generateSessionId();
        this.messageHistory = [];
        this.isTyping = false;
        this.apiStatus = 'ready';
        
        this.initializeElements();
        this.bindEvents();
        this.initializeUI();
        this.testApiConnection();
    }

    /**
     * Initialize DOM element references
     */
    initializeElements() {
        this.elements = {};
        Object.keys(ChatbotConfig.DEFAULT_CONFIG.elements).forEach(key => {
            this.elements[key] = document.querySelector(ChatbotConfig.DEFAULT_CONFIG.elements[key]);
        });
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Message input events
        this.elements.messageInput.addEventListener('input', this.handleInputChange.bind(this));
        this.elements.messageInput.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Send button events
        this.elements.sendButton.addEventListener('click', this.sendMessage.bind(this));
        
        // Header button events
        document.getElementById('clearChatBtn').addEventListener('click', this.clearChat.bind(this));
        document.getElementById('settingsBtn').addEventListener('click', this.openSettings.bind(this));
        
        // Settings modal events
        document.getElementById('closeSettingsBtn').addEventListener('click', this.closeSettings.bind(this));
        document.getElementById('saveSettingsBtn').addEventListener('click', this.saveSettings.bind(this));
        document.getElementById('resetSettingsBtn').addEventListener('click', this.resetSettings.bind(this));
        
        // Modal backdrop click to close
        document.getElementById('settingsModal').addEventListener('click', (e) => {
            if (e.target.id === 'settingsModal') {
                this.closeSettings();
            }
        });
        
        // Toast close button
        document.getElementById('closeToastBtn').addEventListener('click', this.hideErrorToast.bind(this));
        
        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', this.autoResizeTextarea.bind(this));
    }

    /**
     * Initialize UI elements
     */
    initializeUI() {
        // Set welcome message timestamp
        const welcomeTime = document.getElementById('welcomeTime');
        if (welcomeTime) {
            welcomeTime.textContent = ChatbotConfig.formatTimestamp(new Date());
        }
        
        // Update character count
        this.updateCharacterCount();
        
        // Load settings into modal
        this.loadSettingsIntoModal();
    }

    /**
     * Test API connection
     */
    async testApiConnection() {
        try {
            const response = await fetch(this.config.get('apiUrl').replace('/chat', '/health'), {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (response.ok) {
                this.updateApiStatus('connected', 'API: Connected');
            } else {
                this.updateApiStatus('error', 'API: Error');
            }
        } catch (error) {
            this.updateApiStatus('error', 'API: Disconnected');
        }
    }

    /**
     * Handle input change events
     */
    handleInputChange() {
        const message = this.elements.messageInput.value.trim();
        const sendButton = this.elements.sendButton;
        
        // Enable/disable send button
        sendButton.disabled = message.length === 0;
        
        // Update character count
        this.updateCharacterCount();
    }

    /**
     * Handle key down events
     */
    handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    /**
     * Auto-resize textarea
     */
    autoResizeTextarea() {
        const textarea = this.elements.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    /**
     * Update character count display
     */
    updateCharacterCount() {
        const currentLength = this.elements.messageInput.value.length;
        const maxLength = this.config.get('maxMessageLength');
        this.elements.charCount.textContent = `${currentLength}/${maxLength}`;
        
        // Change color if approaching limit
        if (currentLength > maxLength * 0.9) {
            this.elements.charCount.style.color = '#ef4444';
        } else {
            this.elements.charCount.style.color = '#64748b';
        }
    }

    /**
     * Send message to API
     */
    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.elements.messageInput.value = '';
        this.elements.messageInput.style.height = 'auto';
        this.updateCharacterCount();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to API
            const response = await this.sendToApi(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            if (response && response.response) {
                this.addMessage(response.response, 'bot', response);
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting right now. Please check your connection and try again.', 'bot');
            this.showErrorToast('Failed to send message: ' + error.message);
        }
    }

    /**
     * Send message to API endpoint
     */
    async sendToApi(message) {
        const apiUrl = this.config.get('apiUrl');
        const requestBody = {
            message: message,
            session_id: this.sessionId
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Add message to chat
     */
    addMessage(text, sender, metadata = {}) {
        const messageElement = this.createMessageElement(text, sender, metadata);
        this.elements.chatMessages.appendChild(messageElement);
        
        // Add to history
        this.messageHistory.push({
            text,
            sender,
            timestamp: new Date(),
            metadata
        });
        
        // Limit history size
        if (this.messageHistory.length > this.config.get('maxHistory')) {
            this.messageHistory.shift();
        }
        
        // Auto-scroll if enabled
        if (this.config.get('autoScroll')) {
            this.scrollToBottom();
        }
        
        // Update session ID if provided
        if (metadata.session_id) {
            this.sessionId = metadata.session_id;
        }
    }

    /**
     * Create message element
     */
    createMessageElement(text, sender, metadata) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        if (sender === 'user') {
            avatar.innerHTML = '<i class="fas fa-user"></i>';
        } else {
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
        }
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = ChatbotConfig.sanitizeInput(text);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = ChatbotConfig.formatTimestamp(new Date());
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        return messageDiv;
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        this.isTyping = true;
        this.elements.typingIndicator.style.display = 'flex';
        
        if (this.config.get('autoScroll')) {
            this.scrollToBottom();
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        this.isTyping = false;
        this.elements.typingIndicator.style.display = 'none';
    }

    /**
     * Scroll to bottom of chat
     */
    scrollToBottom() {
        const chatMessages = this.elements.chatMessages;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /**
     * Clear chat history
     */
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            // Keep only the welcome message
            const welcomeMessage = this.elements.chatMessages.querySelector('.bot-message');
            this.elements.chatMessages.innerHTML = '';
            if (welcomeMessage) {
                this.elements.chatMessages.appendChild(welcomeMessage);
            }
            
            // Clear message history
            this.messageHistory = [];
            
            // Generate new session ID
            this.sessionId = ChatbotConfig.generateSessionId();
            
            // Show confirmation
            this.showErrorToast('Chat history cleared', 'success');
        }
    }

    /**
     * Open settings modal
     */
    openSettings() {
        document.getElementById('settingsModal').classList.add('show');
        this.loadSettingsIntoModal();
    }

    /**
     * Close settings modal
     */
    closeSettings() {
        document.getElementById('settingsModal').classList.remove('show');
    }

    /**
     * Load current settings into modal
     */
    loadSettingsIntoModal() {
        document.getElementById('apiUrl').value = this.config.get('apiUrl');
        document.getElementById('sessionId').value = this.sessionId || '';
        document.getElementById('maxHistory').value = this.config.get('maxHistory');
        document.getElementById('autoScroll').checked = this.config.get('autoScroll');
    }

    /**
     * Save settings from modal
     */
    saveSettings() {
        const apiUrl = document.getElementById('apiUrl').value.trim();
        const sessionId = document.getElementById('sessionId').value.trim();
        const maxHistory = parseInt(document.getElementById('maxHistory').value);
        const autoScroll = document.getElementById('autoScroll').checked;
        
        // Validate inputs
        if (!ChatbotConfig.isValidApiUrl(apiUrl)) {
            this.showErrorToast('Please enter a valid API URL');
            return;
        }
        
        if (maxHistory < 10 || maxHistory > 100) {
            this.showErrorToast('Max history must be between 10 and 100');
            return;
        }
        
        // Save settings
        this.config.update({
            apiUrl,
            maxHistory,
            autoScroll
        });
        
        if (sessionId) {
            this.sessionId = sessionId;
        }
        
        // Test new API connection
        this.testApiConnection();
        
        // Close modal and show confirmation
        this.closeSettings();
        this.showErrorToast('Settings saved successfully', 'success');
    }

    /**
     * Reset settings to defaults
     */
    resetSettings() {
        if (confirm('Are you sure you want to reset all settings to defaults?')) {
            this.config.reset();
            this.sessionId = ChatbotConfig.generateSessionId();
            this.loadSettingsIntoModal();
            this.testApiConnection();
            this.showErrorToast('Settings reset to defaults', 'success');
        }
    }

    /**
     * Update API status display
     */
    updateApiStatus(status, text) {
        this.apiStatus = status;
        const statusElement = this.elements.apiStatus;
        
        statusElement.textContent = text;
        statusElement.className = `api-status ${status}`;
    }

    /**
     * Show error toast
     */
    showErrorToast(message, type = 'error') {
        const toast = this.elements.errorToast;
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        
        // Change toast color based on type
        if (type === 'success') {
            toast.style.background = '#10b981';
        } else {
            toast.style.background = '#ef4444';
        }
        
        toast.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideErrorToast();
        }, 5000);
    }

    /**
     * Hide error toast
     */
    hideErrorToast() {
        this.elements.errorToast.classList.remove('show');
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatbotApp();
});

// Export for potential external use
window.ChatbotApp = ChatbotApp;
