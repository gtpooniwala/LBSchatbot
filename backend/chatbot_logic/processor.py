import re
from typing import Dict, List, Tuple


class QueryProcessor:
    def __init__(self):
        self.sensitive_keywords = [
            'harassment', 'discrimination', 'mental health', 'depression', 
            'anxiety', 'suicide', 'self-harm', 'abuse', 'emergency', 'crisis',
            'violation', 'misconduct', 'report', 'complaint'
        ]
        
        self.escalation_triggers = [
            'speak to someone', 'talk to staff', 'human help', 'escalate',
            'serious issue', 'urgent', 'emergency', 'complaint'
        ]
    
    def process_query(self, query: str) -> Dict[str, any]:
        """Process and analyze the input query"""
        processed_query = self.clean_query(query)
        
        analysis = {
            'cleaned_query': processed_query,
            'original_query': query,
            'requires_escalation': self.check_escalation_needed(query),
            'is_sensitive': self.check_sensitive_content(query),
            'query_type': self.classify_query_type(processed_query),
            'confidence_threshold': 0.7 if not self.check_sensitive_content(query) else 0.5
        }
        
        return analysis
    
    def clean_query(self, query: str) -> str:
        """Clean and normalize the query"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', query.strip())
        
        # Remove special characters but keep basic punctuation
        cleaned = re.sub(r'[^\w\s\?\!\.\,\-]', '', cleaned)
        
        return cleaned
    
    def check_escalation_needed(self, query: str) -> bool:
        """Check if the query requires human escalation"""
        query_lower = query.lower()
        
        # Check for escalation triggers
        for trigger in self.escalation_triggers:
            if trigger in query_lower:
                return True
        
        # Check for sensitive content
        return self.check_sensitive_content(query)
    
    def check_sensitive_content(self, query: str) -> bool:
        """Check if the query contains sensitive content"""
        query_lower = query.lower()
        
        for keyword in self.sensitive_keywords:
            if keyword in query_lower:
                return True
        
        return False
    
    def classify_query_type(self, query: str) -> str:
        """Classify the type of query"""
        query_lower = query.lower()
        
        # Academic/Assessment related
        if any(word in query_lower for word in ['assignment', 'exam', 'test', 'grade', 'submit', 'deadline', 'assessment', 'deferral']):
            return 'academic'
        
        # Administrative
        elif any(word in query_lower for word in ['transcript', 'enrollment', 'registration', 'fee', 'payment', 'schedule']):
            return 'administrative'
        
        # Technical/Canvas
        elif any(word in query_lower for word in ['canvas', 'login', 'access', 'technical', 'password', 'download']):
            return 'technical'
        
        # Policy related
        elif any(word in query_lower for word in ['policy', 'rule', 'regulation', 'attendance', 'plagiarism', 'integrity']):
            return 'policy'
        
        # General inquiry
        else:
            return 'general'
    
    def format_response_with_sources(self, response: str, sources: List[str]) -> Dict[str, any]:
        """Format the response with source links and escalation info"""
        formatted_response = {
            'answer': response,
            'sources': sources,
            'escalation_available': True,
            'escalation_text': "Need to speak with someone? Contact the Program Office directly.",
            'escalation_link': "mailto:mam-mim@london.edu?subject=Student Inquiry"
        }
        
        return formatted_response
    
    def get_escalation_response(self) -> Dict[str, any]:
        """Get response for queries that require immediate escalation"""
        return {
            'answer': "I understand you have a sensitive or complex issue that requires personal attention. Please contact the Program Office directly using the link below, and a staff member will assist you confidentially.",
            'sources': ["LBS Student Support Services"],
            'escalation_required': True,
            'escalation_text': "Contact Program Office Now",
            'escalation_link': "mailto:mam-mim@london.edu?subject=Urgent Student Support Request"
        }
    
    def validate_response_quality(self, response: str, confidence_score: float, threshold: float = 0.7) -> bool:
        """Validate if the response quality meets the threshold"""
        if confidence_score < threshold:
            return False
        
        # Check if response is too short or generic
        if len(response.strip()) < 50:
            return False
        
        # Check for placeholder text
        if "i don't know" in response.lower() or "cannot provide" in response.lower():
            return False
        
        return True
