import requests
import json

def check_account_balance():
    api_key = "sk-G8lezihhmzPs3xFUdWJ6D9XuWoVuW5sSuDbeXjjw9c0PTXkQ"
    
    print("🔍 Checking Stability AI Account Balance...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    # Try different possible endpoints for balance/credits
    endpoints = [
        ('https://api.stability.ai/v1/user/balance', 'Balance'),
        ('https://api.stability.ai/v1/user/account', 'Account'),
        ('https://api.stability.ai/v1/organization', 'Organization'),
    ]
    
    balance_found = False
    
    for endpoint, name in endpoints:
        try:
            print(f"\nTrying {name} endpoint...")
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name} data retrieved successfully:")
                print(json.dumps(data, indent=2))
                
                # Look for balance/credits information
                if 'credits' in str(data).lower():
                    balance_found = True
                    print(f"💰 Found credit information in {name} endpoint!")
                    
            elif response.status_code == 401:
                print("❌ Unauthorized - Invalid API key")
                return
            elif response.status_code == 403:
                print("❌ Forbidden - Insufficient permissions")
            elif response.status_code == 404:
                print("⚠️  Not found - Endpoint may not exist")
            else:
                print(f"⚠️  Unexpected status: {response.status_code}")
                if response.text:
                    print(f"Response: {response.text[:200]}...")
                    
        except Exception as e:
            print(f"❌ Error with {name} endpoint: {e}")
    
    if not balance_found:
        print("\n" + "=" * 50)
        print("💡 Note: Balance information may not be available through API")
        print("You might need to check your balance directly on the Stability AI website:")
        print("https://platform.stability.ai/account/credits")
    
    # Try to get pricing information
    print("\n" + "=" * 50)
    print("🔍 Checking pricing information...")
    
    try:
        # This might give us information about pricing
        response = requests.get('https://api.stability.ai/v1/engines/list', headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Engine list retrieved. Checking for pricing info...")
            engines = response.json()
            print("Available engines:")
            for engine in engines if isinstance(engines, list) else engines.get('engines', []):
                engine_id = engine.get('id', 'N/A')
                name = engine.get('name', 'N/A')
                print(f"  - {engine_id}: {name}")
        else:
            print(f"⚠️  Could not retrieve engine list: {response.status_code}")
    except Exception as e:
        print(f"❌ Error retrieving engine list: {e}")

if __name__ == "__main__":
    check_account_balance()