import re
from typing import Dict, List, Tuple


class QueryProcessor:
    def __init__(self):
        # TIER 1: Normal queries - AI can handle directly with no special safeguards
        self.normal_topics = [
            'assignment', 'deadline', 'submission', 'canvas', 'login', 'schedule',
            'curriculum', 'course', 'module', 'timetable', 'library', 'resources',
            'career', 'networking', 'events', 'alumni', 'internship', 'job search'
        ]
        
        # TIER 2: Cautious topics - AI provides basic info but strongly recommends human contact
        self.cautious_keywords = [
            'academic misconduct', 'plagiarism violation', 'cheating', 'integrity breach',
            'grade appeal', 'formal complaint', 'dispute', 'conflict', 'unfair treatment',
            'accommodation', 'disability', 'special needs', 'medical condition',
            'financial hardship', 'payment issues', 'scholarship problems',
            'visa', 'immigration', 'work permit', 'legal status',
            'bullying', 'inappropriate behavior', 'uncomfortable situation',
            'mental health', 'stress', 'anxiety', 'depression', 'overwhelmed'
        ]
        
        # TIER 3: Critical/sensitive topics - Direct to resources immediately, no AI discussion
        self.critical_keywords = [
            'suicide', 'self-harm', 'self-injury', 'kill myself', 'end it all',
            'sexual harassment', 'harassment', 'sexual assault', 'rape', 'unwanted touching',
            'discrimination', 'racism', 'sexism', 'prejudice', 'hate crime',
            'domestic violence', 'abuse', 'stalking', 'threatening behavior',
            'mental health crisis', 'breakdown', 'psychotic', 'psychiatric emergency',
            'substance abuse', 'addiction', 'overdose', 'drug problem',
            'emergency', 'urgent help', 'crisis', 'immediate danger'
        ]
        
        # Manual escalation requests
        self.escalation_triggers = [
            'speak to someone', 'talk to staff', 'human help', 'escalate',
            'need to talk', 'counselor', 'advisor', 'dean'
        ]
    
    def process_query(self, query: str) -> Dict[str, any]:
        """Process and analyze the input query with 3-tier safeguard system"""
        processed_query = self.clean_query(query)
        
        # Determine safeguard tier
        safeguard_tier = self.determine_safeguard_tier(query)
        
        analysis = {
            'cleaned_query': processed_query,
            'original_query': query,
            'safeguard_tier': safeguard_tier,
            'requires_immediate_escalation': safeguard_tier == 3,
            'requires_cautious_response': safeguard_tier == 2,
            'query_type': self.classify_query_type(processed_query),
            'confidence_threshold': self.get_confidence_threshold(safeguard_tier)
        }
        
        return analysis
    
    def determine_safeguard_tier(self, query: str) -> int:
        """Determine which safeguard tier applies to the query
        
        Returns:
            1: Normal - AI can handle directly
            2: Cautious - Provide basic info + strong recommendation for human contact
            3: Critical - Direct to resources immediately, no AI discussion
        """
        query_lower = query.lower()
        
        # Check for manual escalation requests first
        for trigger in self.escalation_triggers:
            if trigger in query_lower:
                return 2  # User wants human contact
        
        # Check for Tier 3 (Critical) - Most sensitive topics
        for keyword in self.critical_keywords:
            if keyword in query_lower:
                return 3
        
        # Check for Tier 2 (Cautious) - Moderately sensitive topics
        for keyword in self.cautious_keywords:
            if keyword in query_lower:
                return 2
        
        # Default to Tier 1 (Normal) - Safe topics
        return 1
    
    def get_confidence_threshold(self, safeguard_tier: int) -> float:
        """Get confidence threshold based on safeguard tier"""
        if safeguard_tier == 1:
            return 0.7  # Higher threshold for normal queries
        elif safeguard_tier == 2:
            return 0.5  # Lower threshold, allow more cautious responses
        else:  # Tier 3
            return 0.0  # No threshold needed, direct escalation
    
    def clean_query(self, query: str) -> str:
        """Clean and normalize the query"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', query.strip())
        
        # Remove special characters but keep basic punctuation
        cleaned = re.sub(r'[^\w\s\?\!\.\,\-]', '', cleaned)
        
        return cleaned
    
    def determine_safeguard_tier(self, query: str) -> int:
        """Determine which safeguard tier applies to the query
        
        Returns:
            1: Normal - AI can handle directly
            2: Cautious - Provide basic info + strong recommendation for human contact
            3: Critical - Direct to resources immediately, no AI discussion
        """
        query_lower = query.lower()
        
        # Check for manual escalation requests first
        for trigger in self.escalation_triggers:
            if trigger in query_lower:
                return 2  # User wants human contact
        
        # Check for Tier 3 (Critical) - Most sensitive topics
        for keyword in self.critical_keywords:
            if keyword in query_lower:
                return 3
        
        # Check for Tier 2 (Cautious) - Moderately sensitive topics
        for keyword in self.cautious_keywords:
            if keyword in query_lower:
                return 2
        
        # Default to Tier 1 (Normal) - Safe topics
        return 1
    
    def get_confidence_threshold(self, safeguard_tier: int) -> float:
        """Get confidence threshold based on safeguard tier"""
        if safeguard_tier == 1:
            return 0.7  # Higher threshold for normal queries
        elif safeguard_tier == 2:
            return 0.5  # Lower threshold, allow more cautious responses
        else:  # Tier 3
            return 0.0  # No threshold needed, direct escalation
    
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
        
        # Wellness/Support
        elif any(word in query_lower for word in ['mental health', 'stress', 'anxiety', 'support', 'counseling']):
            return 'wellness'
        
        # General inquiry
        else:
            return 'general'
    
    def get_tier_3_escalation_response(self) -> Dict[str, any]:
        """Get immediate escalation response for Tier 3 queries"""
        return {
            'answer': """I understand you're reaching out about a sensitive matter that requires immediate personal attention. For your safety and wellbeing, please contact the appropriate support services directly:

🆘 **Emergency Services**: If you're in immediate danger, call 999 (UK) or your local emergency number.

🏥 **LBS Student Support**: For urgent student matters, contact the Program Office immediately at mam-mim@london.edu or call during business hours.

💙 **Mental Health Support**: 
- Samaritans (24/7): 116 123 (free, confidential)
- NHS Mental Health Crisis: Text SHOUT to 85258
- LBS Counseling Services: Available through Student Services

Your wellbeing is the top priority. Please reach out for help - you don't have to handle this alone.""",
            'sources': ['LBS Student Support Services', 'Emergency Services', 'Mental Health Resources'],
            'escalation_required': True,
            'escalation_text': 'Get Help Now',
            'escalation_link': 'mailto:mam-mim@london.edu?subject=Urgent Support Request',
            'confidence': 'high',
            'safeguard_tier': 3
        }
    
    def format_response_with_sources(self, response: str, sources: List[str], safeguard_tier: int = 1) -> Dict[str, any]:
        """Format the response with source links and escalation info based on safeguard tier"""
        
        if safeguard_tier == 1:
            # Normal response
            formatted_response = {
                'answer': response,
                'sources': sources,
                'escalation_available': True,
                'escalation_text': "Need more help? Contact the Program Office",
                'escalation_link': "mailto:mam-mim@london.edu?subject=Student Inquiry",
                'safeguard_tier': 1
            }
        
        elif safeguard_tier == 2:
            # Cautious response with strong recommendation for human contact
            enhanced_response = f"""{response}

**⚠️ Important:** This topic often requires personalized guidance. I strongly recommend speaking with a staff member who can provide tailored advice for your specific situation. They can offer confidential support and ensure you get the most appropriate help."""
            
            formatted_response = {
                'answer': enhanced_response,
                'sources': sources,
                'escalation_recommended': True,
                'escalation_text': "Speak with Program Office Staff",
                'escalation_link': "mailto:mam-mim@london.edu?subject=Need Personal Guidance",
                'safeguard_tier': 2
            }
        
        else:  # Tier 3
            # This should use get_tier_3_escalation_response instead
            return self.get_tier_3_escalation_response()
        
        return formatted_response
    
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
