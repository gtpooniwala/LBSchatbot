import requests
import json

# Test real content integration
response = requests.post("http://localhost:5003/api/chat", 
                        json={"message": "What are the official LBS grade classifications for Masters programmes?"})

if response.status_code == 200:
    data = response.json()
    print("RESPONSE:")
    print("Answer:", data.get('answer', 'No answer'))
    print("\nSources:")
    for i, source in enumerate(data.get('sources', []), 1):
        print(f"{i}. {source.get('title', 'Unknown')}")
else:
    print("Error:", response.status_code, response.text)
