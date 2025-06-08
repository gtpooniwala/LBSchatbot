import os
from openai import OpenAI
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"
        
        # System prompt for the LBS chatbot
        self.system_prompt = """You are an AI assistant for London Business School's MAM & MiM Program Office. Your role is to help students with queries about policies, procedures, and academic matters.

IMPORTANT GUIDELINES:
1. Always provide accurate, helpful responses based on the provided context
2. If you cannot find relevant information in the context, politely say so and suggest contacting the Program Office
3. Always maintain a professional, friendly tone
4. For sensitive issues (harassment, mental health, emergencies), direct students to contact the Program Office directly
5. Include specific policy references when available
6. Keep responses concise but comprehensive
7. Always end with an offer to escalate to human staff if needed

Context will be provided for each query. Base your responses strictly on this context."""

    def generate_response(self, query: str, context: str, sources: List[str], query_analysis: Dict) -> Dict[str, any]:
        """Generate a response using OpenAI based on the provided context"""
        
        try:
            # Check if escalation is needed
            if query_analysis.get('requires_escalation', False):
                return self._get_escalation_response()
            
            # Prepare the user message with context
            user_message = self._prepare_user_message(query, context, sources)
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more consistent responses
                max_tokens=500
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Format the response
            formatted_response = {
                "answer": generated_text,
                "sources": sources,
                "escalation_available": True,
                "escalation_text": "Need to speak with someone? Contact the Program Office.",
                "escalation_link": "mailto:mam-mim@london.edu?subject=Student Inquiry",
                "confidence": "high" if context else "low"
            }
            
            return formatted_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response(query)
    
    def _prepare_user_message(self, query: str, context: str, sources: List[str]) -> str:
        """Prepare the user message with context and sources"""
        
        if not context:
            return f"""Student Query: "{query}"

No relevant context found in the knowledge base. Please provide a helpful response directing the student to contact the Program Office for assistance."""
        
        sources_text = "\n".join([f"- {source}" for source in sources]) if sources else "No specific sources available"
        
        user_message = f"""Student Query: "{query}"

Relevant Information from Knowledge Base:
{context}

Sources:
{sources_text}

Please provide a helpful, accurate response based on the above context. Include relevant policy details and always offer escalation to human staff if needed."""
        
        return user_message
    
    def _get_escalation_response(self) -> Dict[str, any]:
        """Get response for queries requiring immediate escalation"""
        return {
            "answer": "I understand you have a sensitive or complex issue that requires personal attention. For matters involving harassment, discrimination, mental health, or other sensitive topics, please contact the Program Office directly. A staff member will assist you confidentially and ensure you receive the appropriate support.",
            "sources": ["LBS Student Support Services"],
            "escalation_required": True,
            "escalation_text": "Contact Program Office Now",
            "escalation_link": "mailto:mam-mim@london.edu?subject=Urgent Student Support Request",
            "confidence": "high"
        }
    
    def _get_fallback_response(self, query: str) -> Dict[str, any]:
        """Get fallback response when OpenAI fails"""
        return {
            "answer": f"I apologize, but I'm experiencing technical difficulties processing your query: '{query}'. Please contact the Program Office directly for assistance, and they'll be happy to help you with your question.",
            "sources": [],
            "escalation_available": True,
            "escalation_text": "Contact Program Office",
            "escalation_link": "mailto:mam-mim@london.edu?subject=Technical Issue - Student Inquiry",
            "confidence": "system_error"
        }
    
    def generate_simple_response(self, query: str) -> str:
        """Generate a simple response without RAG (for testing)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for London Business School students. Provide brief, helpful responses."},
                    {"role": "user", "content": query}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating simple response: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please contact the Program Office for assistance."
