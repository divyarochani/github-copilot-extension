import requests
import json

BASE_URL = 'https://github-copilot-extension-production.up.railway.app'

def test_copilot_format():
    """Test with GitHub Copilot expected format"""
    
    # Test with Copilot message format
    copilot_request = {
        "messages": [
            {
                "role": "user",
                "content": "user info octocat"
            }
        ]
    }
    
    print("🤖 Testing Copilot format...")
    response = requests.post(
        f"{BASE_URL}/copilot/chat",
        json=copilot_request,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Copilot format working!")
        print(f"Response: {result}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == '__main__':
    test_copilot_format()