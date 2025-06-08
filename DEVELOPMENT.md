# LBS RAG Chatbot - Development Guide

## 🛠️ Development Environment Setup

### Prerequisites
- **Python 3.8+** (tested with 3.11)
- **Git** for version control
- **OpenAI API Key** with GPT-3.5-turbo access
- **Text Editor/IDE** (VS Code recommended)

### Quick Setup
```bash
# Clone and setup
git clone <repository-url>
cd generative-ai-chatbot
chmod +x setup.sh
./setup.sh

# Follow setup script instructions
```

## 🏗️ System Architecture Deep Dive

### RAG Pipeline Flow
```
User Query → Query Processing → Safety Classification → Context Retrieval → Response Generation → Safety Filtering → User Response
```

### Component Responsibilities

#### 1. Query Processor (`chatbot_logic/processor.py`)
- **Input Cleaning**: Normalize text, remove artifacts
- **Safety Classification**: 3-tier system (Normal/Cautious/Critical)
- **Intent Analysis**: Academic vs. personal queries
- **Confidence Thresholding**: Dynamic based on safety tier

#### 2. Data Manager (`data_manager.py`)
- **Knowledge Base Loading**: Parse structured text files
- **Embedding Generation**: Sentence-BERT vector creation
- **Semantic Search**: Cosine similarity matching
- **Caching System**: Persistent embedding storage

#### 3. Response Generator (`chatbot_logic/generator.py`)
- **Context Assembly**: Combine retrieved documents with query
- **OpenAI Integration**: GPT-3.5-turbo API calls
- **Source Attribution**: Extract and format citations
- **Safety Formatting**: Tier-appropriate response structure

#### 4. Flask Application (`app.py`)
- **API Endpoints**: RESTful interface for frontend
- **Error Handling**: Graceful failure with fallback responses
- **Logging System**: Interaction tracking and debugging
- **Health Monitoring**: System status endpoints

## 🔍 Code Structure Guidelines

### File Organization
```
backend/
├── app.py                 # Flask app & API routes
├── data_manager.py        # RAG data processing
├── .env                   # Environment variables (not in git)
├── .env.example           # Template for environment setup
├── requirements.txt       # Python dependencies
├── chatbot_logic/
│   ├── processor.py       # Query analysis & safety
│   └── generator.py       # Response generation
└── data/
    ├── knowledge_base.txt # LBS academic content
    └── embeddings_cache.pkl # Vector cache (auto-generated)
```

### Coding Standards

#### Python Style
- **PEP 8** compliance for formatting
- **Type hints** for function parameters and returns
- **Docstrings** for all classes and public methods
- **Error handling** with try/catch blocks
- **Logging** instead of print statements for production

#### Example Function Template
```python
def process_query(self, query: str) -> Dict[str, Any]:
    """
    Process and analyze user query for safety and intent.
    
    Args:
        query (str): Raw user input text
        
    Returns:
        Dict[str, Any]: Analysis results including safety tier
        
    Raises:
        ValueError: If query is empty or invalid
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise
```

#### JavaScript Style
- **ES6+** features (const/let, arrow functions)
- **Async/await** for API calls
- **Error handling** with try/catch
- **DOM manipulation** without jQuery dependency
- **Responsive design** principles

## 🧪 Testing Strategy

### Test Categories

#### 1. Unit Tests
- Individual component functionality
- Safety tier classification accuracy
- Embedding generation consistency
- Response formatting validation

#### 2. Integration Tests
- End-to-end query processing
- API endpoint responses
- Frontend-backend communication
- Error propagation handling

#### 3. System Tests (`test_system.py`)
Current test suite covers:
- Health endpoint connectivity
- Policy query retrieval
- Canvas help responses
- Escalation detection (mental health)
- Academic integrity guidance
- Error handling scenarios

### Running Tests
```bash
# Backend unit tests
cd backend
python -m pytest tests/

# System integration tests
python test_system.py

# Frontend testing (manual)
# Open browser dev tools and test UI interactions
```

### Adding New Tests
```python
def test_new_feature():
    """Test description"""
    # Arrange
    query = "test input"
    expected = "expected output"
    
    # Act
    result = process_function(query)
    
    # Assert
    assert result == expected
    assert "source" in result
```

## 📊 Performance Optimization

### Current Performance Metrics
- **Response Time**: < 3 seconds average
- **Memory Usage**: ~200MB with embeddings cached
- **API Calls**: 1 OpenAI call per query
- **Cache Hit Rate**: 100% for embeddings (after first load)

### Optimization Strategies

#### Backend Optimizations
1. **Embedding Caching**: Persistent storage prevents recomputation
2. **Connection Pooling**: Reuse HTTP connections for OpenAI API
3. **Context Limiting**: Top-3 documents to reduce token usage
4. **Lazy Loading**: Load embeddings only when needed

#### Frontend Optimizations
1. **Debouncing**: Prevent rapid-fire API calls
2. **Response Streaming**: Progressive display of long responses
3. **Asset Optimization**: Minified CSS/JS for production
4. **Caching Headers**: Browser caching for static assets

### Memory Management
```python
# Good: Efficient embedding storage
self.embeddings = np.array(embeddings, dtype=np.float32)

# Good: Release resources after use
del large_temporary_data

# Good: Use generators for large datasets
def process_documents():
    for doc in large_document_set:
        yield process_single_doc(doc)
```

## 🔐 Security Considerations

### API Security
- **CORS Configuration**: Restrict origins to known domains
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent API abuse
- **Error Masking**: Don't expose internal details

### Data Privacy
- **No Persistent Storage**: Conversations not saved permanently
- **API Key Protection**: Environment variables only
- **Audit Logging**: Track access without storing content
- **GDPR Compliance**: No personal data retention

### Safety Measures
```python
# Input sanitization
def clean_query(self, query: str) -> str:
    # Remove potentially harmful characters
    cleaned = re.sub(r'[<>]', '', query)
    return cleaned.strip()[:1000]  # Limit length

# Safe API calls
def call_openai_api(self, prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            timeout=30  # Prevent hanging
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return self.get_fallback_response()
```

## 🚀 Deployment Guide

### Development Deployment
```bash
# Backend (Terminal 1)
cd backend
source ../venv/bin/activate
export OPENAI_API_KEY="your-key"
python app.py

# Frontend (Terminal 2)
cd frontend
python -m http.server 8000
```

### Production Deployment

#### Using Gunicorn (Recommended)
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5003 app:app
```

#### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt

EXPOSE 5003
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5003", "app:app"]
```

#### Environment Variables for Production
```bash
export OPENAI_API_KEY="your-production-key"
export DEBUG_MODE="False"
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5003"
```

## 🐛 Debugging & Troubleshooting

### Common Issues

#### 1. OpenAI API Errors
```python
# Debug API connectivity
import openai
try:
    openai.Model.list()
    print("✓ OpenAI API accessible")
except Exception as e:
    print(f"✗ OpenAI API error: {e}")
```

#### 2. Embedding Cache Issues
```bash
# Clear and regenerate embeddings
rm backend/data/embeddings_cache.pkl
# Restart backend server
```

#### 3. Frontend Connection Issues
```javascript
// Check API connectivity
fetch('http://localhost:5003/health')
  .then(response => response.json())
  .then(data => console.log('Backend status:', data))
  .catch(error => console.error('Connection error:', error));
```

### Debug Mode
Enable verbose logging in `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.run(debug=True)
```

### Performance Profiling
```python
import cProfile
import pstats

def profile_query_processing():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    result = process_query("test query")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

## 📈 Feature Development

### Adding New Knowledge
1. Edit `backend/data/knowledge_base.txt`
2. Use markdown formatting with `---` separators
3. Include source citations: `[Title](URL)`
4. Restart backend to reload content

### Adding New Safety Keywords
```python
# In processor.py
self.cautious_keywords.extend([
    'new_sensitive_topic',
    'another_careful_keyword'
])
```

### Adding New API Endpoints
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        data = request.get_json()
        # Process request
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Frontend Feature Development
```javascript
// Add new UI component
function addNewFeature() {
    const featureDiv = document.createElement('div');
    featureDiv.className = 'new-feature';
    featureDiv.innerHTML = 'New feature content';
    document.getElementById('target').appendChild(featureDiv);
}
```

## 📚 Knowledge Base Management

### Content Structure
```markdown
### Policy: Title Here
Detailed policy description with clear guidelines.
Multiple paragraphs explaining the policy.

**Contact Information:**
- Phone: +44 (0)20 7000 XXXX
- Email: service@london.edu

Source: [Policy Name](https://lbs.edu/policy-url)

---
```

### Best Practices
- **Clear Headings**: Use consistent formatting
- **Contact Details**: Always include relevant contacts
- **Source Attribution**: Link to official LBS resources
- **Regular Updates**: Keep information current
- **Comprehensive Coverage**: Address common student queries

## 🤝 Contributing Guidelines

### Pull Request Process
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/new-feature`
3. **Test** your changes thoroughly
4. **Document** new features in README
5. **Submit** pull request with clear description

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass (run `python test_system.py`)
- [ ] Documentation updated
- [ ] No sensitive data in commits
- [ ] Performance impact considered
- [ ] Security implications reviewed

---

## 📞 Support Channels

### Development Support
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: This guide and README.md
- **Code Comments**: Inline documentation in source files

### LBS Integration Support
- **Program Office**: Academic content and policy updates
- **IT Services**: Infrastructure and deployment support
- **Student Feedback**: User experience and feature requests

---

*Last Updated: June 8, 2025*
