#!/usr/bin/env python3
"""
Quick test script for LBS RAG Chatbot
Simple test for basic functionality and real content integration
"""

import requests
import json

def quick_test():
    """Run a quick test of the chatbot functionality"""
    
    print("🚀 Quick Test - LBS RAG Chatbot")
    print("=" * 40)
    
    # Test real content integration
    query = "What are the official LBS grade classifications for Masters programmes?"
    print(f"🔍 Testing query: {query}")
    
    try:
        response = requests.post(
            "http://localhost:5003/api/chat", 
            json={"message": query},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("\n✅ RESPONSE RECEIVED:")
            print("📄 Answer:", data.get('answer', 'No answer'))
            print("\n📚 Sources:")
            for i, source in enumerate(data.get('sources', []), 1):
                print(f"   {i}. {source}")
            
            if data.get('sources'):
                print("\n✅ Real content integration working!")
            else:
                print("\n⚠️  No sources found - check knowledge base")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure the backend server is running on port 5003")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🏁 Quick test completed")

if __name__ == "__main__":
    quick_test()
