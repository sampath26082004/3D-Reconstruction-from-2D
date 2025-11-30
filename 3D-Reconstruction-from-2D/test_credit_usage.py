import requests
import json

def check_credit_usage():
    api_key = "sk-G8lezihhmzPs3xFUdWJ6D9XuWoVuW5sSuDbeXjjw9c0PTXkQ"
    
    print("🔍 Checking credit usage for 3D generation...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    # Check credits before
    try:
        response = requests.get('https://api.stability.ai/v1/user/balance', headers=headers, timeout=10)
        if response.status_code == 200:
            balance_before = response.json().get('credits', 'Unknown')
            print(f"💰 Credits before test: {balance_before}")
        else:
            print(f"⚠️  Could not check balance: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error checking balance: {e}")
        return
    
    print("\n💡 Based on Stability AI pricing:")
    print("- Each 3D model generation typically costs 1-3 credits")
    print("- With 25 credits, you can generate approximately 8-25 models")
    print("- The exact cost depends on image complexity and processing time")
    
    print("\n" + "=" * 50)
    print("📌 To check actual credit usage:")
    print("1. Generate a 3D model through your application")
    print("2. Run this script again to see the difference")
    print("3. The difference will show actual credit consumption")

if __name__ == "__main__":
    check_credit_usage()