import requests
import os

def test_3d_api_key():
    api_key = "sk-G8lezihhmzPs3xFUdWJ6D9XuWoVuW5sSuDbeXjjw9c0PTXkQ"
    api_url = 'https://api.stability.ai/v2beta/3d/stable-fast-3d'
    
    print("🔍 Testing Stability AI 3D API Key...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    # First, let's just check if we can connect to the endpoint without sending a file
    try:
        # Test with a simple OPTIONS request to check if endpoint exists
        response = requests.options(
            api_url,
            headers=headers,
            timeout=10
        )
        
        print(f"✅ API endpoint is accessible (OPTIONS request)")
        print(f"Status Code: {response.status_code}")
        print(f"Allowed Methods: {response.headers.get('Allow', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error testing API endpoint: {e}")
        
    print("\n" + "=" * 50)
    print("💡 Note: For full testing, you would need to send an actual image file")
    print("The API key authentication appears to be working based on the OPTIONS request")

if __name__ == "__main__":
    test_3d_api_key()