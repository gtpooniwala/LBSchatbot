// This file contains the JavaScript code for handling user interactions with the chatbot, including sending queries to the backend and displaying responses.

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const messagesDiv = document.getElementById('messages');
    const newChatBtn = document.getElementById('new-chat-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const historySidebar = document.getElementById('history-sidebar');
    const chatHistoryList = document.getElementById('chat-history-list');

    // Backend API URL
    const API_URL = 'http://localhost:5003';
    
    // Chat session management
    let currentSessionId = generateSessionId();
    let chatSessions = loadChatSessions();
    
    // Initialize the interface
    initializeInterface();
    
    function generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    function loadChatSessions() {
        const stored = localStorage.getItem('lbs_chat_sessions');
        if (stored) {
            return JSON.parse(stored);
        }
        
        // Return dummy data if no sessions exist
        return {
            'session_1': {
                id: 'session_1',
                title: 'Assignment Extensions Policy',
                timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
                messages: [
                    { content: 'How do I request an assignment extension?', isUser: true, timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() },
                    { content: 'You can request an assignment extension for documented extenuating circumstances. Requests must be submitted at least 48 hours before the deadline via the online Extension Request Form. Extensions may be granted for medical or personal emergencies with appropriate documentation.', isUser: false, timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000 + 5000).toISOString(), sources: ['LBS Assessment Guidelines'] }
                ]
            },
            'session_2': {
                id: 'session_2',
                title: 'Canvas Submission Help',
                timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
                messages: [
                    { content: 'I\'m having trouble submitting my assignment on Canvas', isUser: true, timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString() },
                    { content: 'For Canvas submission issues, please check: 1) File format matches requirements (PDF, Word, etc.), 2) File size is under 100MB, 3) You\'re submitting before the deadline. You should receive an email confirmation upon successful submission. If problems persist, contact IT Support.', isUser: false, timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000 + 5000).toISOString(), sources: ['Canvas Assignment Submission Guide'] }
                ]
            },
            'session_3': {
                id: 'session_3',
                title: 'MiM Program Structure',
                timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(), // 5 hours ago
                messages: [
                    { content: 'What are the core modules in the MiM program?', isUser: true, timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString() },
                    { content: 'The Master in Management (MiM) program includes Foundation modules (Accounting, Economics, Statistics), Core modules (Strategy, Marketing, Operations, Finance, Organizational Behavior), and Elective modules. You\'ll also complete a summer internship and a final Capstone Project.', isUser: false, timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000 + 5000).toISOString(), sources: ['MiM Program Handbook'] }
                ]
            }
        };
    }
    
    function saveChatSessions() {
        localStorage.setItem('lbs_chat_sessions', JSON.stringify(chatSessions));
    }
    
    function initializeInterface() {
        // Create current session if it doesn't exist
        if (!chatSessions[currentSessionId]) {
            chatSessions[currentSessionId] = {
                id: currentSessionId,
                title: 'New Chat',
                timestamp: new Date().toISOString(),
                messages: []
            };
            saveChatSessions();
        }
        
        renderChatHistory();
        loadSession(currentSessionId);
        
        // Add welcome message for new sessions
        if (chatSessions[currentSessionId].messages.length === 0) {
            setTimeout(() => {
                addWelcomeMessage();
            }, 500);
        }
    }
    
    function renderChatHistory() {
        chatHistoryList.innerHTML = '';
        
        // Sort sessions by timestamp (newest first)
        const sortedSessions = Object.values(chatSessions).sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        );
        
        sortedSessions.forEach(session => {
            const historyItem = document.createElement('div');
            historyItem.className = 'chat-history-item';
            if (session.id === currentSessionId) {
                historyItem.classList.add('active');
            }
            
            const title = document.createElement('div');
            title.className = 'chat-title';
            title.textContent = session.title;
            
            const time = document.createElement('div');
            time.className = 'chat-time';
            time.textContent = formatTimestamp(session.timestamp);
            
            historyItem.appendChild(title);
            historyItem.appendChild(time);
            
            historyItem.addEventListener('click', () => loadSession(session.id));
            
            chatHistoryList.appendChild(historyItem);
        });
    }
    
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffTime = now - date;
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
            return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString();
        }
    }
    
    function loadSession(sessionId) {
        currentSessionId = sessionId;
        const session = chatSessions[sessionId];
        
        // Clear current messages
        messagesDiv.innerHTML = '';
        
        // Load session messages
        session.messages.forEach(msg => {
            addMessage(msg.content, msg.isUser, msg.sources || [], msg.escalationLink || null, false);
        });
        
        // Update active state in history
        renderChatHistory();
        
        // Scroll to bottom
        setTimeout(() => {
            messagesDiv.scrollTo({
                top: messagesDiv.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }
    
    function createNewChat() {
        currentSessionId = generateSessionId();
        chatSessions[currentSessionId] = {
            id: currentSessionId,
            title: 'New Chat',
            timestamp: new Date().toISOString(),
            messages: []
        };
        saveChatSessions();
        
        // Clear current messages
        messagesDiv.innerHTML = '';
        
        // Update UI
        renderChatHistory();
        
        // Add welcome message
        setTimeout(() => {
            addWelcomeMessage();
        }, 300);
        
        // Focus input
        userInput.focus();
    }
    
    function clearCurrentChat() {
        if (confirm('Are you sure you want to clear this chat? This action cannot be undone.')) {
            chatSessions[currentSessionId].messages = [];
            chatSessions[currentSessionId].title = 'New Chat';
            chatSessions[currentSessionId].timestamp = new Date().toISOString();
            saveChatSessions();
            
            messagesDiv.innerHTML = '';
            renderChatHistory();
            
            setTimeout(() => {
                addWelcomeMessage();
            }, 300);
        }
    }
    
    function updateSessionTitle(sessionId, firstMessage) {
        if (chatSessions[sessionId] && chatSessions[sessionId].title === 'New Chat') {
            // Generate title from first message (truncated)
            let title = firstMessage.substring(0, 30);
            if (firstMessage.length > 30) {
                title += '...';
            }
            chatSessions[sessionId].title = title;
            chatSessions[sessionId].timestamp = new Date().toISOString();
            saveChatSessions();
            renderChatHistory();
        }
    }    function addMessage(content, isUser = false, sources = [], escalationLink = null, saveToSession = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Create message content
        const contentDiv = document.createElement('div');
        if (isUser) {
            contentDiv.textContent = content; // Keep user messages as plain text
        } else {
            // For bot messages, format newlines and bullet points properly
            console.log('Original content:', JSON.stringify(content)); // Debug line
            const formattedContent = content
                .replace(/\\n/g, '<br>')  // Handle escaped newlines
                .replace(/\n/g, '<br>')   // Handle actual newlines
                .replace(/- /g, '• ')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold text
            console.log('Formatted content:', formattedContent); // Debug line
            contentDiv.innerHTML = formattedContent;
        }
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

        // Save to session if requested
        if (saveToSession) {
            const messageData = {
                content,
                isUser,
                timestamp: new Date().toISOString(),
                sources: sources || [],
                escalationLink: escalationLink || null
            };
            
            chatSessions[currentSessionId].messages.push(messageData);
            
            // Update session title if this is the first user message
            if (isUser && chatSessions[currentSessionId].messages.filter(m => m.isUser).length === 1) {
                updateSessionTitle(currentSessionId, content);
            }
            
            saveChatSessions();
        }

        // Smooth scroll to bottom with animation
        setTimeout(() => {
            messagesDiv.scrollTo({
                top: messagesDiv.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }
    
    function addWelcomeMessage() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <h3 style="margin-top: 0; color: var(--lbs-deep-blue);">👋 Welcome to the LBS Student Assistant!</h3>
            <p>I'm here to help with your London Business School MAM & MiM program queries.</p>
            <p><strong>I can assist with:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>Academic policies and procedures</li>
                <li>Canvas and assignment submissions</li>
                <li>Program requirements and deadlines</li>
                <li>General academic questions</li>
            </ul>
            <p style="margin-bottom: 0;"><em>How can I help you today?</em></p>
        `;
        messagesDiv.appendChild(welcomeDiv);
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Disable send button to prevent multiple submissions
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing';
        typingDiv.textContent = 'Thinking...';
        messagesDiv.appendChild(typingDiv);
        
        // Smooth scroll to show typing indicator
        setTimeout(() => {
            messagesDiv.scrollTo({
                top: messagesDiv.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
        
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
        })
        .finally(() => {
            // Re-enable send button
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send';
            userInput.focus(); // Return focus to input
        });
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent newline
            sendMessage();
        }
    });

    // New chat button
    newChatBtn.addEventListener('click', createNewChat);
    
    // Clear chat button
    clearChatBtn.addEventListener('click', clearCurrentChat);
    
    // Sidebar toggle for mobile
    sidebarToggle.addEventListener('click', () => {
        historySidebar.classList.toggle('open');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            !historySidebar.contains(e.target) && 
            !sidebarToggle.contains(e.target) &&
            historySidebar.classList.contains('open')) {
            historySidebar.classList.remove('open');
        }
    });

    // Focus on input when page loads
    userInput.focus();
});
