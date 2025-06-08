from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from datetime import datetime

# Import our custom modules
from data_manager import DataManager
from chatbot_logic.processor import QueryProcessor
from chatbot_logic.generator import ResponseGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize components
print("Initializing RAG chatbot components...")
try:
    data_manager = DataManager()
    query_processor = QueryProcessor()
    response_generator = ResponseGenerator()
    print("All components initialized successfully!")
except Exception as e:
    print(f"Error initializing components: {e}")
    data_manager = None
    query_processor = None
    response_generator = None

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get the query from request
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'error': 'Empty query provided'}), 400
        
        # Log the query
        print(f"Received query: {user_query}")
        
        # Check if components are initialized
        if not all([data_manager, query_processor, response_generator]):
            return jsonify({
                'response': "I'm currently experiencing technical difficulties. Please contact the Program Office directly for assistance.",
                'sources': [],
                'escalation_link': "mailto:mam-mim@london.edu?subject=Technical Issue"
            })
        
        # Process the query
        query_analysis = query_processor.process_query(user_query)
        print(f"Query analysis: {query_analysis}")
        
        # Check for immediate escalation
        if query_analysis.get('requires_escalation', False):
            escalation_response = query_processor.get_escalation_response()
            return jsonify(escalation_response)
        
        # Get relevant context from knowledge base
        context, sources = data_manager.get_context_for_query(query_analysis['cleaned_query'])
        print(f"Found {len(sources)} relevant sources")
        
        # Generate response using OpenAI
        response_data = response_generator.generate_response(
            query=user_query,
            context=context,
            sources=sources,
            query_analysis=query_analysis
        )
        
        # Log the interaction
        log_interaction(user_query, response_data)
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        print(traceback.format_exc())
        
        # Return error response
        error_response = {
            'response': "I apologize, but I encountered an error processing your request. Please contact the Program Office directly for assistance.",
            'sources': [],
            'escalation_available': True,
            'escalation_text': "Contact Program Office",
            'escalation_link': "mailto:mam-mim@london.edu?subject=Technical Error - Student Inquiry"
        }
        
        return jsonify(error_response), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'data_manager': data_manager is not None,
            'query_processor': query_processor is not None,
            'response_generator': response_generator is not None
        }
    }
    
    if data_manager:
        status['knowledge_base'] = {
            'documents_loaded': len(data_manager.documents),
            'embeddings_ready': data_manager.embeddings is not None
        }
    
    return jsonify(status)

@app.route('/api/test', methods=['POST'])
def test_simple():
    """Simple test endpoint without full RAG"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if response_generator:
            simple_response = response_generator.generate_simple_response(user_query)
            return jsonify({'response': simple_response})
        else:
            return jsonify({'response': 'Test endpoint working, but OpenAI not initialized'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def log_interaction(query: str, response_data: dict):
    """Log chat interactions for analysis"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response_data.get('answer', ''),
            'sources_count': len(response_data.get('sources', [])),
            'escalation_triggered': response_data.get('escalation_required', False)
        }
        
        # You can extend this to write to a file or database
        print(f"Logged interaction: {json.dumps(log_entry, indent=2)}")
        
    except Exception as e:
        print(f"Error logging interaction: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
