import requests
import json

# Test the Flask app locally
BASE_URL = 'http://localhost:5000'

def test_chat_endpoint():
    """Test the chat endpoint with different commands"""
    
    test_cases = [
        {"message": "user info octocat"},
        {"message": "repo info microsoft/vscode"},
        {"message": "search python web framework"},
        {"message": "help"}
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['message']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{BASE_URL}/copilot/chat",
                json=test_case,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result['response']}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed. Make sure the Flask app is running.")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n🏥 Testing health endpoint")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed: {result}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == '__main__':
    print("🚀 Starting tests...")
    test_health_endpoint()
    test_chat_endpoint()
    print("\n✨ Tests completed!")