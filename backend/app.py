from flask import Flask, request, jsonify
from chatbot_logic.generator import ResponseGenerator
from chatbot_logic.processor import QueryProcessor
from data_manager import load_knowledge_base, log_chat

app = Flask(__name__)

# Load knowledge base
knowledge_base = load_knowledge_base('data/knowledge_base.txt')

# Initialize chatbot components
response_generator = ResponseGenerator(knowledge_base)
query_processor = QueryProcessor()

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query')
    processed_query = query_processor.process_query(user_query)
    response = response_generator.generate_response(processed_query)
    
    # Log the chat
    log_chat('data/chat_logs.txt', f'User: {user_query}\nBot: {response}\n')
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)