// This file contains the JavaScript code for handling user interactions with the chatbot, including sending queries to the backend and displaying responses.

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const messagesDiv = document.getElementById('messages');

    // Backend API URL
    const API_URL = 'http://localhost:5001';

    function addMessage(content, isUser = false, sources = [], escalationLink = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Create message content
        const contentDiv = document.createElement('div');
        contentDiv.textContent = content;
        messageDiv.appendChild(contentDiv);
        
        // Add sources if available
        if (!isUser && sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources';
            sourcesDiv.innerHTML = '<strong>Sources:</strong>';
            
            const sourcesList = document.createElement('ul');
            sources.forEach(source => {
                const listItem = document.createElement('li');
                // Check if source contains a link
                if (source.includes('http') || source.includes('[') && source.includes(']')) {
                    listItem.innerHTML = source;
                } else {
                    listItem.textContent = source;
                }
                sourcesList.appendChild(listItem);
            });
            
            sourcesDiv.appendChild(sourcesList);
            messageDiv.appendChild(sourcesDiv);
        }
        
        // Add escalation link if available
        if (!isUser && escalationLink) {
            const escalationDiv = document.createElement('div');
            escalationDiv.className = 'escalation';
            escalationDiv.innerHTML = `<a href="${escalationLink}" target="_blank">Need more help? Contact the Program Office →</a>`;
            messageDiv.appendChild(escalationDiv);
        }
        
        messagesDiv.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing';
        typingDiv.textContent = 'Thinking...';
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        // Send to backend
        fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            messagesDiv.removeChild(typingDiv);
            
            // Handle different response formats
            let responseText = '';
            let sources = [];
            let escalationLink = null;
            
            if (data.answer) {
                // New RAG format
                responseText = data.answer;
                sources = data.sources || [];
                escalationLink = data.escalation_link || null;
            } else if (data.response) {
                // Fallback format
                responseText = data.response;
            } else {
                responseText = 'Sorry, I received an unexpected response format.';
            }
            
            addMessage(responseText, false, sources, escalationLink);
        })
        .catch(error => {
            // Remove typing indicator
            if (typingDiv.parentNode) {
                messagesDiv.removeChild(typingDiv);
            }
            
            console.error('Error:', error);
            addMessage('Sorry, there was an error connecting to the server. Please try again or contact the Program Office directly.', false, [], 'mailto:mam-mim@london.edu?subject=Technical Issue');
        });
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Add a welcome message
    addMessage('Hello! I\'m here to help with your London Business School MAM & MiM program queries. I can assist with policies, procedures, assignments, and general academic questions. How can I help you today?', false);
});
