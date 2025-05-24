// This file contains the JavaScript code for handling user interactions with the chatbot, including sending queries to the backend and displaying responses.

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatOutput = document.getElementById('chat-output');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userQuery = chatInput.value;
        chatInput.value = '';

        displayMessage('You: ' + userQuery);
        sendQueryToBackend(userQuery);
    });

    function sendQueryToBackend(query) {
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage('Bot: ' + data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('Bot: Sorry, there was an error processing your request.');
        });
    }

    function displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatOutput.appendChild(messageElement);
    }
});