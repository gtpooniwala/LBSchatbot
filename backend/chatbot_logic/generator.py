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
7. Adapt your response tone based on the safeguard tier provided

SAFEGUARD TIERS:
- Tier 1 (Normal): Provide comprehensive, helpful responses
- Tier 2 (Cautious): Provide basic info but emphasize human support is recommended
- Tier 3 (Critical): Should not reach here - handle via immediate escalation

Context will be provided for each query. Base your responses strictly on this context."""

    def generate_response(self, query: str, context: str, sources: List[str], query_analysis: Dict) -> Dict[str, any]:
        """Generate a response using OpenAI based on the provided context and safeguard tier"""
        
        try:
            # Check safeguard tier from query analysis
            safeguard_tier = query_analysis.get('safeguard_tier', 1)
            
            # Tier 3: Immediate escalation - don't generate AI response
            if safeguard_tier == 3:
                return query_analysis.get('tier_3_response', self._get_tier_3_escalation_response())
            
            # Tier 2 & 1: Generate AI response with appropriate guidance
            user_message = self._prepare_user_message(query, context, sources, safeguard_tier)
            
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
            
            # Format response based on safeguard tier
            if safeguard_tier == 2:
                # Tier 2: Cautious response with strong recommendation for human contact
                enhanced_response = f"""{generated_text}

**⚠️ Important:** This topic often requires personalized guidance. I strongly recommend speaking with a staff member who can provide tailored advice for your specific situation."""
                
                formatted_response = {
                    "answer": enhanced_response,
                    "sources": sources,
                    "escalation_recommended": True,
                    "escalation_text": "Speak with Program Office Staff",
                    "escalation_link": "mailto:mam-mim@london.edu?subject=Need Personal Guidance",
                    "confidence": "medium",
                    "safeguard_tier": 2
                }
            else:
                # Tier 1: Normal response
                formatted_response = {
                    "answer": generated_text,
                    "sources": sources,
                    "escalation_available": True,
                    "escalation_text": "Need more help? Contact the Program Office",
                    "escalation_link": "mailto:mam-mim@london.edu?subject=Student Inquiry",
                    "confidence": "high" if context else "low",
                    "safeguard_tier": 1
                }
            
            return formatted_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response(query)
    
    def _prepare_user_message(self, query: str, context: str, sources: List[str], safeguard_tier: int = 1) -> str:
        """Prepare the user message with context and sources, adjusted for safeguard tier"""
        
        if not context:
            # Check if this is a "what can you help with" type query
            query_lower = query.lower()
            if any(phrase in query_lower for phrase in ['what can you', 'what do you', 'what are you', 'help me with', 'tell me about', 'what topics', 'what information']):
                return f"""Student Query: "{query}"
Safeguard Tier: {safeguard_tier}

This appears to be a query asking about the chatbot's capabilities. Please provide a comprehensive overview of what the LBS MAM & MiM Program Office chatbot can help with, including:

- Academic policies and procedures
- Course information and curriculum details
- Assessment guidelines and deadlines
- Student services and support
- Canvas and IT support
- Career services and professional development
- Administrative procedures
- Library and learning resources
- International student support
- Mental health and wellbeing resources

Make it welcoming and informative, showing the breadth of topics covered."""
            else:
                return f"""Student Query: "{query}"
Safeguard Tier: {safeguard_tier}

No relevant context found in the knowledge base. Please provide a helpful response explaining that while you don't have specific information about this topic, you can help with many other student-related queries, and suggest contacting the Program Office for this specific question."""
        
        sources_text = "\n".join([f"- {source}" for source in sources]) if sources else "No specific sources available"
        
        # Add tier-specific guidance
        tier_guidance = ""
        if safeguard_tier == 2:
            tier_guidance = "\n\nIMPORTANT: This is a Tier 2 (Cautious) query. Provide helpful information but emphasize that personal guidance from staff is strongly recommended."
        elif safeguard_tier == 1:
            tier_guidance = "\n\nThis is a Tier 1 (Normal) query. Provide comprehensive, helpful information."
        
        user_message = f"""Student Query: "{query}"
Safeguard Tier: {safeguard_tier}

Relevant Information from Knowledge Base:
{context}

Sources:
{sources_text}{tier_guidance}

Please provide a helpful, accurate response based on the above context. Include relevant policy details and appropriate escalation guidance."""
        
        return user_message
    
    def _get_tier_3_escalation_response(self) -> Dict[str, any]:
        """Get immediate escalation response for Tier 3 critical queries"""
        return {
            "answer": """I understand you're reaching out about a sensitive matter that requires immediate personal attention. For your safety and wellbeing, please contact the appropriate support services directly:

🆘 **Emergency Services**: If you're in immediate danger, call 999 (UK) or your local emergency number.

🏥 **LBS Student Support**: For urgent student matters, contact the Program Office immediately at mam-mim@london.edu or call during business hours.

💙 **Mental Health Support**: 
- Samaritans (24/7): 116 123 (free, confidential)
- NHS Mental Health Crisis: Text SHOUT to 85258
- LBS Counseling Services: Available through Student Services

Your wellbeing is the top priority. Please reach out for help - you don't have to handle this alone.""",
            "sources": ['LBS Student Support Services', 'Emergency Services', 'Mental Health Resources'],
            "escalation_required": True,
            "escalation_text": 'Get Help Now',
            "escalation_link": 'mailto:mam-mim@london.edu?subject=Urgent Support Request',
            "confidence": 'high',
            "safeguard_tier": 3
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
