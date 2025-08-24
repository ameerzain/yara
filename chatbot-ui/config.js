/**
 * Configuration file for the Chatbot UI
 * Contains default settings and configuration management
 */

const DEFAULT_CONFIG = {
    // API Configuration
    apiUrl: 'http://localhost:8000/chat',
    
    // Session Configuration
    sessionId: null, // Will be auto-generated if null
    
    // UI Configuration
    maxHistory: 50,
    autoScroll: true,
    
    // Message Configuration
    maxMessageLength: 1000,
    typingDelay: 1000, // Delay before showing typing indicator
    
    // Error Handling
    maxRetries: 3,
    retryDelay: 1000,
    
    // UI Elements
    elements: {
        chatMessages: '#chatMessages',
        messageInput: '#messageInput',
        sendButton: '#sendButton',
        typingIndicator: '#typingIndicator',
        charCount: '#charCount',
        apiStatus: '#apiStatus',
        settingsModal: '#settingsModal',
        errorToast: '#errorToast'
    }
};

/**
 * Configuration Manager Class
 * Handles loading, saving, and managing configuration settings
 */
class ConfigManager {
    constructor() {
        this.config = { ...DEFAULT_CONFIG };
        this.loadConfig();
    }

    /**
     * Load configuration from localStorage
     */
    loadConfig() {
        try {
            const savedConfig = localStorage.getItem('chatbotConfig');
            if (savedConfig) {
                const parsed = JSON.parse(savedConfig);
                this.config = { ...DEFAULT_CONFIG, ...parsed };
            }
        } catch (error) {
            console.warn('Failed to load saved configuration:', error);
        }
    }

    /**
     * Save configuration to localStorage
     */
    saveConfig() {
        try {
            localStorage.setItem('chatbotConfig', JSON.stringify(this.config));
        } catch (error) {
            console.warn('Failed to save configuration:', error);
        }
    }

    /**
     * Get a configuration value
     * @param {string} key - Configuration key
     * @returns {*} Configuration value
     */
    get(key) {
        return this.config[key];
    }

    /**
     * Set a configuration value
     * @param {string} key - Configuration key
     * @param {*} value - Configuration value
     */
    set(key, value) {
        this.config[key] = value;
        this.saveConfig();
    }

    /**
     * Reset configuration to defaults
     */
    reset() {
        this.config = { ...DEFAULT_CONFIG };
        this.saveConfig();
    }

    /**
     * Get all configuration
     * @returns {Object} Complete configuration object
     */
    getAll() {
        return { ...this.config };
    }

    /**
     * Update multiple configuration values at once
     * @param {Object} updates - Object containing configuration updates
     */
    update(updates) {
        this.config = { ...this.config, ...updates };
        this.saveConfig();
    }
}

/**
 * Generate a unique session ID
 * @returns {string} Unique session ID
 */
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Format timestamp for display
 * @param {Date|string|number} timestamp - Timestamp to format
 * @returns {string} Formatted timestamp string
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // If less than 24 hours, show time
    if (diff < 24 * 60 * 60 * 1000) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // If less than 7 days, show day name
    if (diff < 7 * 24 * 60 * 60 * 1000) {
        return date.toLocaleDateString([], { weekday: 'short' });
    }
    
    // Otherwise show date
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
}

/**
 * Validate API URL format
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid, false otherwise
 */
function isValidApiUrl(url) {
    try {
        const parsed = new URL(url);
        return parsed.protocol === 'http:' || parsed.protocol === 'https:';
    } catch {
        return false;
    }
}

/**
 * Sanitize user input to prevent XSS
 * @param {string} input - User input to sanitize
 * @returns {string} Sanitized input
 */
function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export configuration and utilities
window.ChatbotConfig = {
    DEFAULT_CONFIG,
    ConfigManager,
    generateSessionId,
    formatTimestamp,
    isValidApiUrl,
    sanitizeInput,
    debounce,
    throttle
};
