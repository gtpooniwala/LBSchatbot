# LBS RAG Chatbot - API Documentation

This document provides comprehensive API documentation for the LBS RAG Chatbot backend services.

## 📋 Overview

The LBS RAG Chatbot API is a RESTful service built with Flask that provides intelligent academic support through a Retrieval-Augmented Generation (RAG) pipeline. The API integrates OpenAI's GPT-3.5-turbo with a comprehensive knowledge base of LBS academic policies and support services.

### Base URL
```
Development: http://localhost:5003
Production: https://your-domain.com
```

### API Version
```
Version: 2.0
Last Updated: June 2025
```

## 🔐 Authentication

Currently, the API does not require authentication for basic usage. However, rate limiting is implemented to prevent abuse.

### Rate Limits
- **Default**: 60 requests per minute per IP
- **Burst**: Up to 20 additional requests in short bursts
- **Headers**: Rate limit information is included in response headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1623456789
```

## 🚀 Endpoints

### 1. Chat Endpoint

Primary endpoint for chatbot interactions.

#### POST /api/chat

Processes user queries and returns AI-generated responses with source citations and appropriate safety measures.

##### Request

**Headers:**
```http
Content-Type: application/json
```

**Body:**
```json
{
    "query": "What is the attendance policy for MAM students?"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | User's question or request (max 1000 characters) |

##### Response

**Success Response (200 OK):**

For normal academic queries (Tier 1):
```json
{
    "response": "Students are required to attend at least 80% of all scheduled classes and seminars. Failure to meet this requirement without prior approval may result in a failing grade for the module. Exceptions may be granted for documented medical or personal emergencies. Students must notify the Program Office within 48 hours of any anticipated absence.",
    "sources": [
        "LBS Student Handbook, Page 12 - https://lbs.edu/handbook"
    ],
    "query_analysis": {
        "safeguard_tier": 1,
        "requires_escalation": false,
        "query_type": "academic_policy",
        "confidence_threshold": 0.7
    },
    "metadata": {
        "response_time": 2.3,
        "documents_retrieved": 3,
        "ai_model": "gpt-3.5-turbo"
    }
}
```

For sensitive queries requiring caution (Tier 2):
```json
{
    "response": "⚠️ Important: I understand you're going through a difficult time. While I can provide some general information, I strongly recommend speaking directly with our Student Wellness Centre for personalized support and professional guidance.\n\nThe LBS Student Wellness Centre provides confidential counselling and mental health support. They have trained professionals who can provide much better assistance than I can.",
    "sources": [
        "LBS Student Wellbeing - https://lbs.edu/student-wellbeing"
    ],
    "escalation_available": true,
    "escalation_text": "Contact Student Wellness Centre",
    "escalation_link": "tel:+442070008500",
    "escalation_email": "wellness@london.edu",
    "query_analysis": {
        "safeguard_tier": 2,
        "requires_escalation": true,
        "query_type": "mental_health",
        "confidence_threshold": 0.5
    }
}
```

For critical situations requiring immediate help (Tier 3):
```json
{
    "response": "I'm very concerned about your wellbeing and want to make sure you get immediate, professional support. Please contact one of these crisis resources right away:",
    "sources": [],
    "crisis_resources": [
        "Emergency Services: 999",
        "Samaritans: 116 123 (Free, 24/7, confidential)",
        "LBS Student Welfare Emergency: +44 (0)20 7000 8999"
    ],
    "immediate_escalation": true,
    "professional_help_required": true,
    "query_analysis": {
        "safeguard_tier": 3,
        "requires_escalation": true,
        "query_type": "crisis_situation"
    }
}
```

**Error Responses:**

400 Bad Request - Invalid input:
```json
{
    "error": "Empty query provided",
    "message": "Query parameter is required and cannot be empty"
}
```

429 Too Many Requests - Rate limit exceeded:
```json
{
    "error": "Rate limit exceeded",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
}
```

500 Internal Server Error - System error:
```json
{
    "error": "Internal server error",
    "message": "I apologize, but I encountered an error processing your request. Please contact the Program Office directly for assistance.",
    "escalation_link": "mailto:mam-mim@london.edu?subject=Technical Error"
}
```

##### Example Usage

**cURL:**
```bash
curl -X POST http://localhost:5003/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I submit assignments on Canvas?"}'
```

**JavaScript (Fetch):**
```javascript
const response = await fetch('http://localhost:5003/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        query: 'What are the requirements for the MAM program?'
    })
});

const data = await response.json();
console.log(data.response);
```

**Python (Requests):**
```python
import requests

response = requests.post(
    'http://localhost:5003/api/chat',
    json={'query': 'I need help with my mental health'},
    headers={'Content-Type': 'application/json'}
)

data = response.json()
print(data['response'])
```

### 2. Health Check Endpoint

System health monitoring endpoint.

#### GET /health

Returns the current system status and component health.

##### Request

No parameters required.

##### Response

**Success Response (200 OK):**
```json
{
    "status": "healthy",
    "timestamp": "2025-06-08T14:30:45Z",
    "version": "2.0",
    "components": {
        "data_manager": "operational",
        "query_processor": "operational",
        "response_generator": "operational",
        "openai_api": "connected"
    },
    "knowledge_base": {
        "documents_loaded": 7,
        "embeddings_cached": true,
        "last_updated": "2025-06-08T10:15:30Z"
    },
    "system_info": {
        "python_version": "3.11.5",
        "flask_version": "2.3.3",
        "uptime_seconds": 86400
    }
}
```

**Error Response (503 Service Unavailable):**
```json
{
    "status": "unhealthy",
    "timestamp": "2025-06-08T14:30:45Z",
    "components": {
        "data_manager": "error",
        "query_processor": "operational",
        "response_generator": "error",
        "openai_api": "disconnected"
    },
    "errors": [
        "OpenAI API connection failed",
        "Knowledge base not loaded"
    ]
}
```

##### Example Usage

**cURL:**
```bash
curl http://localhost:5003/health
```

**JavaScript:**
```javascript
const health = await fetch('http://localhost:5003/health');
const status = await health.json();
console.log(status.status); // "healthy" or "unhealthy"
```

### 3. Test Endpoint

Simple test endpoint for basic connectivity testing.

#### POST /api/test

Provides a simple echo response for testing API connectivity without full RAG processing.

##### Request

**Body:**
```json
{
    "message": "test"
}
```

##### Response

**Success Response (200 OK):**
```json
{
    "status": "success",
    "message": "Test endpoint working",
    "echo": "test",
    "timestamp": "2025-06-08T14:30:45Z"
}
```

## 🔧 Query Processing Pipeline

### 1. Input Validation
- Query length validation (max 1000 characters)
- HTML/script tag sanitization
- Rate limiting enforcement

### 2. Safety Classification
The system analyzes queries using a 3-tier classification:

**Tier 1 - Normal Queries:**
- Academic policies and procedures
- Canvas and technology help
- General program information
- Career and academic support

**Tier 2 - Cautious Queries:**
- Mental health and stress
- Academic misconduct concerns
- Financial difficulties
- Disability accommodations
- Immigration and visa issues

**Tier 3 - Critical Queries:**
- Self-harm or suicide indicators
- Sexual harassment or assault
- Discrimination reports
- Domestic violence or abuse
- Psychiatric emergencies

### 3. Knowledge Retrieval
- Semantic search using sentence transformers
- Top 3 most relevant documents retrieved
- Minimum similarity threshold: 0.3
- Source attribution for all responses

### 4. Response Generation
- Context-aware prompting with OpenAI GPT-3.5-turbo
- Professional, LBS-appropriate tone
- Proper source citations included
- Escalation links for sensitive topics

## 📊 Response Formats

### Standard Response Fields

| Field | Type | Description |
|-------|------|-------------|
| response | string | Main AI-generated response text |
| sources | array | List of source citations with links |
| query_analysis | object | Query classification and metadata |
| escalation_available | boolean | Whether human escalation is recommended |
| escalation_text | string | Text for escalation button/link |
| escalation_link | string | URL/phone/email for escalation |
| escalation_email | string | Direct email for escalation |
| crisis_resources | array | Emergency contact information |
| immediate_escalation | boolean | Whether immediate help is required |
| metadata | object | Response timing and system info |

### Query Analysis Object

| Field | Type | Description |
|-------|------|-------------|
| safeguard_tier | integer | Safety classification (1, 2, or 3) |
| requires_escalation | boolean | Whether human intervention is needed |
| query_type | string | Classified type of query |
| confidence_threshold | float | Similarity threshold used for retrieval |

## 🚨 Error Handling

### Error Response Format
```json
{
    "error": "error_type",
    "message": "Human-readable error description",
    "code": "ERROR_CODE",
    "details": {
        "additional": "context"
    }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| EMPTY_QUERY | 400 | Query parameter is empty or missing |
| QUERY_TOO_LONG | 400 | Query exceeds maximum length limit |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests from client |
| OPENAI_API_ERROR | 502 | OpenAI API is unavailable |
| KNOWLEDGE_BASE_ERROR | 503 | Knowledge base is not loaded |
| INTERNAL_ERROR | 500 | Unexpected system error |

## 🔧 Configuration

### Environment Variables

The API behavior can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | - | OpenAI API key (required) |
| OPENAI_MODEL | gpt-3.5-turbo | OpenAI model to use |
| OPENAI_MAX_TOKENS | 1000 | Maximum tokens in response |
| OPENAI_TEMPERATURE | 0.7 | Response creativity (0.0-1.0) |
| SIMILARITY_THRESHOLD | 0.3 | Minimum similarity for document retrieval |
| TOP_K_DOCUMENTS | 3 | Number of documents to retrieve |
| RATE_LIMIT_PER_MINUTE | 60 | API rate limit per IP |
| LOG_LEVEL | INFO | Logging verbosity |

## 📈 Performance Considerations

### Response Times
- **Normal queries**: < 3 seconds average
- **Complex queries**: < 5 seconds average
- **Health check**: < 100ms

### Optimization Features
- **Embedding Cache**: Vector embeddings cached for faster retrieval
- **Connection Pooling**: Efficient API connection management
- **Rate Limiting**: Prevents system overload
- **Error Caching**: Graceful degradation during outages

## 🧪 Testing

### Unit Tests
```bash
# Run backend tests
cd backend
python test_system.py
```

### Integration Tests
```bash
# Test full API workflow
curl -X POST http://localhost:5003/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "test query"}'
```

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5003/health

# Using wrk
wrk -t12 -c400 -d30s http://localhost:5003/api/chat
```

## 📝 SDKs and Examples

### Python SDK Example
```python
import requests
from typing import Dict, Any

class LBSChatbotClient:
    def __init__(self, base_url: str = "http://localhost:5003"):
        self.base_url = base_url
    
    def chat(self, query: str) -> Dict[str, Any]:
        """Send a chat query to the LBS Chatbot API"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the chatbot service"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# Usage
client = LBSChatbotClient()
result = client.chat("What is the attendance policy?")
print(result['response'])
```

### JavaScript SDK Example
```javascript
class LBSChatbotClient {
    constructor(baseUrl = 'http://localhost:5003') {
        this.baseUrl = baseUrl;
    }
    
    async chat(query) {
        const response = await fetch(`${this.baseUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
}

// Usage
const client = new LBSChatbotClient();
const result = await client.chat("How do I submit assignments?");
console.log(result.response);
```

## 🔄 Webhooks (Future Enhancement)

Future versions may include webhook support for real-time notifications:

```json
{
    "url": "https://your-app.com/webhook",
    "events": ["escalation_triggered", "crisis_detected"],
    "secret": "webhook_secret"
}
```

## 📞 Support

### API Support
- **Technical Issues**: Contact IT Support (+44 20 7000 7100)
- **System Status**: Check `/health` endpoint
- **Documentation**: This API documentation

### Business Support
- **Content Updates**: Program Office (mam-mim@london.edu)
- **Emergency Escalation**: Student Welfare (+44 20 7000 8999)

---

**API Version**: 2.0  
**Last Updated**: June 8, 2025  
**Maintained By**: LBS IT Department
