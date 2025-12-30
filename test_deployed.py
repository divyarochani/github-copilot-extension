import requests
import json

# Test the deployed app
BASE_URL = 'https://github-copilot-extension-production.up.railway.app'

def test_deployed_app():
    """Test the deployed Flask app"""
    
    print("🚀 Testing deployed GitHub Copilot Extension")
    print("=" * 50)
    
    # Test homepage
    print("\n1. Testing homepage...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Homepage working!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage error: {e}")
    
    # Test health check
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check working!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test chat endpoint
    print("\n3. Testing chat functionality...")
    test_messages = [
        "user info octocat",
        "repo info microsoft/vscode", 
        "search python web framework",
        "help"
    ]
    
    for message in test_messages:
        print(f"\n📝 Testing: '{message}'")
        try:
            response = requests.post(
                f"{BASE_URL}/copilot/chat",
                json={"message": message},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response: {result['response'][:100]}...")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_deployed_app()