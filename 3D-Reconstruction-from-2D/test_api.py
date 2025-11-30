import requests

def test_api_key():
    api_key = "sk-G8lezihhmzPs3xFUdWJ6D9XuWoVuW5sSuDbeXjjw9c0PTXkQ"
    
    print("🔍 Testing Stability AI API Key...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    try:
        # Test the 3D API endpoint
        response = requests.get(
            'https://api.stability.ai/v2beta/3d/stable-fast-3d',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API Key is valid and working!")
            print("✅ 3D API endpoint is accessible")
        elif response.status_code == 401:
            print("❌ API Key is invalid or unauthorized")
            print("Response:", response.text)
        elif response.status_code == 403:
            print("❌ API Key is valid but lacks permissions")
            print("Response:", response.text)
        else:
            print(f"⚠️  API returned status code: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_api_key()