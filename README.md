# Generative AI-Driven Chatbot

This project is a Generative AI-driven chatbot that utilizes a separate front-end and back-end architecture. The chatbot is designed to interact with users, providing responses based on a knowledge base stored in text files. 

## Project Structure

```
generative-ai-chatbot
├── backend
│   ├── app.py
│   ├── chatbot_logic
│   │   ├── generator.py
│   │   └── processor.py
│   └── data_manager.py
├── frontend
│   ├── index.html
│   ├── css
│   │   └── style.css
│   └── js
│       └── script.js
├── data
│   ├── knowledge_base.txt
│   └── chat_logs.txt
└── README.md
```

## Features

- **Generative AI Responses**: The chatbot uses advanced generative AI techniques to create contextually relevant responses based on user queries.
- **Knowledge Base**: The chatbot's responses are informed by a knowledge base that can be easily updated through a text file.
- **User Interaction**: A user-friendly front-end interface allows users to interact with the chatbot seamlessly.

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd generative-ai-chatbot
   ```

2. **Backend Setup**:
   - Navigate to the `backend` directory.
   - Install the required dependencies (e.g., Flask, any AI libraries).
   - Run the backend application:
     ```
     python app.py
     ```

3. **Frontend Setup**:
   - Open `frontend/index.html` in a web browser to access the chatbot interface.

## Usage Guidelines

- Users can type their queries into the chatbot interface.
- The chatbot processes the queries and generates responses based on the knowledge base.
- Interaction logs are stored in `data/chat_logs.txt` for future reference.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.