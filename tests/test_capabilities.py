#!/usr/bin/env python3
"""
Test script for LBS RAG Chatbot capability queries
Verifies that the chatbot properly responds to "what can you help with" type queries
"""

import requests
import json

def test_capabilities_query():
    """Test that the chatbot properly responds to capability queries"""
    
    url = "http://localhost:5003/api/chat"
    
    test_queries = [
        "What can you tell me about?",
        "What can you help me with?",
        "What topics do you cover?",
        "What information is available?"
    ]
    
    print("🧪 Testing Chatbot Capability Queries")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query}'")
        print("-" * 40)
        
        try:
            response = requests.post(url, json={"message": query}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                sources = data.get('sources', [])
                
                print(f"✅ Response received ({len(answer)} chars)")
                print(f"📚 Sources: {len(sources)}")
                print(f"📄 Answer preview: {answer[:300]}...")
                
                # Check if response contains helpful information
                if any(keyword in answer.lower() for keyword in ['academic', 'policies', 'student', 'help', 'canvas', 'career']):
                    print("✅ Response contains helpful capability information")
                else:
                    print("❌ Response may not be helpful enough")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Capability query test completed")

if __name__ == "__main__":
    test_capabilities_query()
