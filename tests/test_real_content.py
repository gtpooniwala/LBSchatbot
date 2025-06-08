#!/usr/bin/env python3
"""
Test script for LBS RAG Chatbot real content integration
Verifies that official LBS documents are properly integrated and accessible
"""

import requests
import json

def test_real_content():
    """Test that the real LBS content is properly integrated"""
    
    url = "http://localhost:5003/api/chat"
    
    # Test queries for real content
    test_queries = [
        "What are the official LBS grade classifications for Masters programmes?",
        "What is the resit policy and grade caps?", 
        "What qualifies as extenuating circumstances at LBS?",
        "What is the minimum pass requirement for Masters programmes?"
    ]
    
    print("🧪 Testing Real LBS Content Integration")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            response = requests.post(url, json={"message": query})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received ({len(data.get('answer', ''))} chars)")
                print(f"📚 Sources: {len(data.get('sources', []))}")
                print(f"📄 Answer preview: {data.get('answer', '')[:200]}...")
                if data.get('sources'):
                    print(f"🔗 Source titles: {[s.get('title', 'Unknown') for s in data.get('sources', [])]}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Real content integration test completed")

if __name__ == "__main__":
    test_real_content()
