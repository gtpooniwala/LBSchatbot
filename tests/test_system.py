#!/usr/bin/env python3
"""
Comprehensive test script for the LBS RAG Chatbot system
Tests all major functionality including RAG pipeline, escalation, and error handling
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5003"
TEST_QUERIES = [
    {
        "query": "What is the attendance policy?",
        "expected_sources": True,
        "expected_escalation": False,
        "description": "Policy query test"
    },
    {
        "query": "How do I submit assignments on Canvas?",
        "expected_sources": True,
        "expected_escalation": False,
        "description": "Canvas functionality test"
    },
    {
        "query": "I am experiencing harassment from another student",
        "expected_sources": False,
        "expected_escalation": True,
        "description": "Escalation detection test"
    },
    {
        "query": "What are the plagiarism rules?",
        "expected_sources": True,
        "expected_escalation": False,
        "description": "Academic integrity test"
    },
    {
        "query": "Random nonsense query about flying elephants",
        "expected_sources": False,
        "expected_escalation": False,
        "description": "Irrelevant query test"
    }
]

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data['status']}")
            print(f"   Documents loaded: {health_data['knowledge_base']['documents_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat_query(query_data):
    """Test a single chat query"""
    print(f"🔍 Testing: {query_data['description']}")
    print(f"   Query: {query_data['query']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            json={"message": query_data["query"]}
        )
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            return False
        
        data = response.json()
        
        # Check response structure
        if "answer" not in data:
            print("❌ Missing 'answer' field in response")
            return False
        
        # Check sources expectation
        has_sources = len(data.get("sources", [])) > 0
        if query_data["expected_sources"] and not has_sources:
            print("❌ Expected sources but none found")
            return False
        elif not query_data["expected_sources"] and has_sources:
            print("⚠️  Unexpected sources found (not necessarily an error)")
        
        # Check escalation expectation
        has_escalation = data.get("escalation_required", False)
        if query_data["expected_escalation"] and not has_escalation:
            print("❌ Expected escalation but none triggered")
            return False
        elif not query_data["expected_escalation"] and has_escalation:
            print("⚠️  Unexpected escalation triggered")
        
        print(f"✅ Test passed!")
        print(f"   Answer length: {len(data['answer'])} characters")
        print(f"   Sources found: {len(data.get('sources', []))}")
        print(f"   Escalation triggered: {has_escalation}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("🔍 Testing error handling...")
    
    # Test empty query
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            json={}
        )
        
        if response.status_code == 400:
            print("✅ Empty query handling works")
        else:
            print(f"❌ Expected 400 for empty query, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    # Test malformed JSON
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            data="invalid json"
        )
        
        if response.status_code >= 400:
            print("✅ Malformed JSON handling works")
        else:
            print(f"❌ Expected error for malformed JSON, got {response.status_code}")
    except Exception as e:
        print("✅ Malformed JSON properly rejected")
    
    return True

def run_all_tests():
    """Run all system tests"""
    print("🚀 Starting LBS RAG Chatbot System Tests")
    print("=" * 50)
    print(f"Test started at: {datetime.now().isoformat()}")
    print()
    
    total_tests = 0
    passed_tests = 0
    
    # Test health endpoint
    total_tests += 1
    if test_health_endpoint():
        passed_tests += 1
    print()
    
    # Test chat queries
    for query_data in TEST_QUERIES:
        total_tests += 1
        if test_chat_query(query_data):
            passed_tests += 1
        time.sleep(1)  # Brief pause between tests
    
    # Test error handling
    total_tests += 1
    if test_error_handling():
        passed_tests += 1
    print()
    
    # Summary
    print("=" * 50)
    print(f"🏁 Test Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The RAG chatbot system is working correctly.")
        return True
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
