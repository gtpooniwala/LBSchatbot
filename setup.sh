#!/bin/bash

# LBS RAG Chatbot - Setup Script
# This script helps set up the development environment

echo "🎓 LBS RAG Chatbot Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python found: $python_version${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd backend
pip install -r requirements.txt
cd ..

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Check for OpenAI API key
echo -e "${BLUE}Checking OpenAI API key...${NC}"
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ OpenAI API key not found in environment variables${NC}"
    echo -e "${YELLOW}Please set your OpenAI API key:${NC}"
    echo -e "${YELLOW}export OPENAI_API_KEY='your-api-key-here'${NC}"
    echo -e "${YELLOW}Or create a .env file in the backend directory${NC}"
else
    echo -e "${GREEN}✓ OpenAI API key found${NC}"
fi

# Create .env template if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo -e "${BLUE}Creating .env template...${NC}"
    cat > backend/.env << EOF
# LBS RAG Chatbot Environment Variables
# Copy this file and add your actual API key

OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG_MODE=True
EOF
    echo -e "${GREEN}✓ .env template created in backend/.env${NC}"
    echo -e "${YELLOW}Please edit backend/.env and add your OpenAI API key${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "${YELLOW}1. Set your OpenAI API key in backend/.env${NC}"
echo -e "${YELLOW}2. Start the backend server:${NC}"
echo "   cd backend && python app.py"
echo ""
echo -e "${YELLOW}3. Start the frontend server (in a new terminal):${NC}"
echo "   cd frontend && python -m http.server 8000"
echo ""
echo -e "${YELLOW}4. Open your browser to: http://localhost:8000${NC}"
echo ""
echo -e "${BLUE}For more information, see README.md${NC}"
