# LBS RAG Chatbot - Academic Support System

A sophisticated **Retrieval-Augmented Generation (RAG)** chatbot designed for London Business School's Master in Analytics and Management (MAM) & Master in Management (MiM) programs. This system provides 24/7 automated support for student queries using real LBS academic policies and procedures.

## 🎯 System Overview

### Core Functionality

- **🤖 Intelligent Query Handling**: Uses OpenAI's GPT-3.5-turbo to provide accurate, context-aware responses
- **📄 Knowledge Base**: This public version integrates dummy LBS documents covering academic policies, Canvas support, and student services. The official version uses official LBS Documents covering the same policies.
- **📚 Real Academic Policy Integration**: Direct access to LBS academic regulations and extenuating circumstances policies from PDF documents
- **💻 Canvas Support**: Comprehensive help with learning management system functionality
- **📞 Contact Information**: Direct access to LBS support services (wellness, career, IT, program office)
- **🛡️ 3-Tier Safety System**: Intelligent escalation for sensitive queries including mental health crisis intervention
- **📖 Source Attribution**: All responses include proper citations with clickable links to official documents

### Key Features

- **Vector-based Semantic Search**: Uses sentence transformers for intelligent document retrieval
- **Real-time Response Generation**: OpenAI GPT-3.5-turbo with LBS-specific context
- **Multi-turn Conversation Memory**: Maintains context across conversation turns
- **Crisis Escalation**: Immediate routing for mental health emergencies and harassment reports
- **Professional Boundaries**: Appropriate handling of irrelevant queries
- **Responsive Design**: Modern chat interface optimized for all devices

## 🏗️ Architecture

```text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Frontend       │    │  Flask Backend   │    │  OpenAI GPT     │
│  (Port 8080)    │◄──►│  (Port 5003)     │◄──►│  3.5-turbo      │
│                 │    │                  │    │                 │
│ • LBS Branding  │    │ • RAG Pipeline   │    │ • Response Gen  │
│ • Chat History  │    │ • Safety System  │    │ • Context Aware │
│ • Responsive UI │    │ • Source Linking │    │ • Crisis Detection│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Knowledge Base  │
                       │   (37 Documents) │
                       │ • Academic Policies│
                       │ • Canvas Guides   │
                       │ • Support Contacts│
                       │ • Emergency Info  │
                       │ • Real PDF Content│
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Semantic Search  │
                       │                  │
                       │ • Sentence Trans │
                       │ • Vector Embeddings│
                       │ • Similarity Match│
                       │ • Smart Truncation│
                       └──────────────────┘
```

## 🛡️ 3-Tier Safety System

### Tier 1: Normal Queries (AI Direct Response)

- **Topics**: Academic policies, Canvas help, schedules, career guidance, grade inquiries
- **Response**: Comprehensive answers with source citations
- **Examples**: "What are the grade classifications?" | "How do I submit assignments?"

### Tier 2: Sensitive Queries (AI + Escalation Options)

- **Topics**: Grade appeals, academic misconduct, financial hardship
- **Response**: Helpful information + escalation button to Program Office
- **Safety**: Dual support approach with immediate human contact option

### Tier 3: Crisis Queries (Immediate Escalation)

- **Topics**: Mental health emergencies, harassment, discrimination, safety concerns
- **Response**: Immediate escalation with crisis support contacts
- **Keywords**: Self-harm, suicide, harassment, discrimination, abuse

## 📊 Real Data Integration

### Official PDF Documents Integrated

1. **Academic Regulations (v2024-1.0)**: Complete academic policies, procedures, and requirements
2. **Extenuating Circumstances Policy (v2024-1.0)**: Detailed guidance on what qualifies, application process, and evidence requirements

### Knowledge Base Statistics

- **37 Documents**: Comprehensive coverage of student needs
- **Real Grade Classifications**: Official LBS grading systems
- **Updated Policies**: Current 2024 academic year regulations
- **Source Attribution**: All content properly cited with links

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
pip install -r requirements.txt

# OpenAI API Key (set in environment)
export OPENAI_API_KEY="your-api-key-here"
```

### Setup & Run

```bash
# Clone repository
git clone <repository-url>
cd generative-ai-chatbot

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
cd backend
python app.py
# Server runs on http://localhost:5003

# Start frontend server (new terminal)
cd frontend
python -m http.server 8080
# Frontend runs on http://localhost:8080
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
OPENAI_MODEL=gpt-3.5-turbo  # Default model
MAX_CONTEXT_LENGTH=3000     # Context window size
```

## 🧪 Testing & Verification

### Quick System Test

```bash
# Test backend health
curl http://localhost:5003/health

# Test chat functionality
curl -X POST http://localhost:5003/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What can you help me with?"}'
```

### Automated Testing Scripts

The system includes comprehensive test scripts for validation and quality assurance:

#### 🚀 **Quick Test** (`tests/quick_test.py`)

```bash
python tests/quick_test.py
```

- **Purpose**: Fast validation of basic functionality
- **Tests**: Real content integration with grade classifications query
- **Runtime**: ~10 seconds
- **Use Case**: Quick health check during development

#### 🧪 **Capability Tests** (`tests/test_capabilities.py`)

```bash
python tests/test_capabilities.py
```

- **Purpose**: Verify chatbot responds properly to "what can you help with" queries
- **Tests**: 4 different capability queries
- **Validates**: Response quality, helpfulness, and content coverage
- **Use Case**: Ensure users get proper guidance on system capabilities

#### 📚 **Real Content Tests** (`tests/test_real_content.py`)

```bash
python tests/test_real_content.py
```

- **Purpose**: Validate integration of official LBS documents
- **Tests**: Grade classifications, resit policies, extenuating circumstances
- **Validates**: Source attribution, accurate content retrieval
- **Use Case**: Confirm official PDF content is accessible and accurate

#### 🔧 **System Tests** (`tests/test_system.py`)

```bash
python tests/test_system.py
```

- **Purpose**: Comprehensive end-to-end system validation
- **Tests**: Health endpoint, chat functionality, escalation detection, error handling
- **Validates**: Full RAG pipeline, safety system, API responses
- **Use Case**: Complete system verification before deployment

#### Test Results Format

All test scripts provide detailed output including:

- ✅ **Pass/Fail Status**: Clear indicators for each test
- 📊 **Metrics**: Response times, content length, source counts
- 🔍 **Details**: Answer previews, source titles, escalation flags
- 📈 **Summary**: Overall test results and recommendations

## 📁 Project Structure

```text
generative-ai-chatbot/
├── README.md                    # This file
├── requirements.txt            # Python dependencies
├── DEMO_QUESTIONS_COPY_PASTE.md # Demo conversation scripts
├── tests/                      # Testing scripts
│   ├── quick_test.py          # Fast functionality validation
│   ├── test_capabilities.py   # Capability query testing
│   ├── test_real_content.py   # Real content integration tests
│   └── test_system.py         # Comprehensive system tests
├── tools/                      # Utility scripts
│   └── extract_pdf.py         # PDF content extraction tool
├── backend/
│   ├── app.py                  # Flask API server
│   ├── data_manager.py         # Knowledge base & search
│   ├── chatbot_logic/
│   │   ├── generator.py        # Response generation
│   │   └── processor.py        # Query processing & safety
│   └── data/
│       ├── knowledge_base.txt  # Main knowledge base
│       ├── Academic Regulations*.pdf # Real LBS documents
│       ├── Extenuating Circumstances*.pdf
│       └── embeddings_cache.pkl # Vector embeddings cache
└── frontend/
    ├── index.html              # Chat interface
    ├── css/style.css          # Styling
    └── js/script.js           # Frontend logic
```

## ⚙️ Configuration

### Backend Configuration

- **Port**: 5003 (configurable in `app.py`)
- **Knowledge Base**: `backend/data/knowledge_base.txt`
- **Vector Model**: `all-MiniLM-L6-v2` (sentence transformers)
- **Context Length**: 3000 characters (supports long documents)

### Frontend Configuration

- **Port**: 8080 (configurable)
- **API Endpoint**: `http://localhost:5003/api/chat`
- **Styling**: Professional LBS branding
- **Features**: Message history, typing indicators, source display

## 🔧 Key Components

### Data Manager (`data_manager.py`)

- **Document Loading**: Parses knowledge base into searchable chunks
- **Vector Embeddings**: Creates and caches document embeddings
- **Semantic Search**: Finds relevant documents using cosine similarity
- **Smart Truncation**: Handles long documents without losing context

### Query Processor (`processor.py`)

- **Safety Classification**: 3-tier system for query handling
- **Crisis Detection**: Keyword-based identification of sensitive topics
- **Query Cleaning**: Normalizes input for better search results
- **Escalation Logic**: Determines appropriate response level

### Response Generator (`generator.py`)

- **Context Assembly**: Combines relevant documents with user query
- **OpenAI Integration**: Sends context to GPT-3.5-turbo for response
- **Source Attribution**: Adds proper citations to all responses
- **Formatting**: Ensures professional, readable output with bullet points

## 📈 Performance & Capabilities

### Response Quality

- **High Accuracy**: Responses based on official LBS documents
- **Proper Citations**: All answers include source attribution
- **Professional Tone**: LBS-appropriate language and formatting
- **Comprehensive Coverage**: 37 documents covering student needs

### System Performance

- **Fast Search**: Vector similarity search in <100ms
- **Efficient Caching**: Embeddings cached for quick startup
- **Scalable Architecture**: Can handle multiple concurrent users
- **Robust Error Handling**: Graceful fallbacks for all failure modes

### Safety Features

- **Crisis Intervention**: Immediate escalation for mental health emergencies
- **Professional Boundaries**: Appropriate handling of irrelevant queries
- **Confidential Support**: Direct routing to appropriate LBS services
- **Audit Trail**: All interactions logged for quality assurance

## 🎯 Use Cases

### For Students

- **Policy Questions**: "What qualifies as extenuating circumstances?"
- **Canvas Help**: "How do I submit my assignment?"
- **Grade Inquiries**: "What are the official grade classifications?"
- **Crisis Support**: Immediate help for mental health concerns

### For Staff

- **Reduced Workload**: 24/7 automated responses to routine queries
- **Quality Assurance**: All responses based on official documents
- **Escalation Management**: Automatic routing of complex issues
- **Usage Analytics**: Insights into common student concerns

## 🔒 Security & Privacy

- **Data Protection**: No personal information stored
- **Secure API**: HTTPS-ready architecture
- **Audit Logging**: All interactions recorded for quality purposes
- **Professional Standards**: Responses maintain LBS confidentiality policies

## 📞 Support

- **System Issues**: Check logs in `backend/` directory
- **Content Updates**: Modify `backend/data/knowledge_base.txt`
- **Configuration**: Update environment variables
- **Emergency**: Contact LBS IT Support

## 📄 License

This project is proprietary to London Business School. All rights reserved.

---

**Status: Production Ready** ✅ | **Last Updated**: 8 June 2025 | **Version**: 2.0
