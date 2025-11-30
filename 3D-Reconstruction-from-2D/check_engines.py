import requests

def check_engines():
    api_key = "sk-G8lezihhmzPs3xFUdWJ6D9XuWoVuW5sSuDbeXjjw9c0PTXkQ"
    
    print("🔍 Checking Stability AI Engines...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    try:
        # Check available engines
        response = requests.get(
            'https://api.stability.ai/v1/engines/list',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            engines_data = response.json()
            print("✅ Successfully retrieved engines list:")
            if isinstance(engines_data, list):
                # Direct list of engines
                for engine in engines_data:
                    print(f"  - {engine.get('id', 'N/A')}: {engine.get('name', 'N/A')} ({engine.get('type', 'N/A')})")
            else:
                # Dictionary with engines key
                for engine in engines_data.get('engines', []):
                    print(f"  - {engine.get('id', 'N/A')}: {engine.get('name', 'N/A')} ({engine.get('type', 'N/A')})")
        elif response.status_code == 401:
            print("❌ Invalid API key")
        elif response.status_code == 403:
            print("❌ API key lacks permissions")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking engines: {e}")

if __name__ == "__main__":
    check_engines()