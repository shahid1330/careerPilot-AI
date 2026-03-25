"""
API Testing Script - Tests all backend endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_result(endpoint, method, response):
    """Print formatted test result"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {method} {endpoint}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json() if response.headers.get('content-type') == 'application/json' else response.text, indent=2)[:200]}")
    print(f"{'='*60}")

def test_apis():
    """Test all API endpoints"""
    
    print("\n🚀 Starting API Tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result("/", "GET", response)
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test 2: Health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_result("/health", "GET", response)
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test 3: Daily quote (requires auth)
    try:
        response = requests.get(f"{BASE_URL}/api/daily-quote")
        print_result("/api/daily-quote", "GET", response)
    except Exception as e:
        print(f"❌ Daily quote endpoint failed: {e}")
    
    # Test 4: Mock test history (requires auth)
    try:
        response = requests.get(f"{BASE_URL}/api/mock-tests/history")
        print_result("/api/mock-tests/history", "GET", response)
    except Exception as e:
        print(f"❌ Mock test history failed: {e}")
    
    # Test 5: Performance summary (requires auth)
    try:
        response = requests.get(f"{BASE_URL}/api/performance/summary")
        print_result("/api/performance/summary", "GET", response)
    except Exception as e:
        print(f"❌ Performance summary failed: {e}")
    
    print("\n✅ API Testing Complete!")

if __name__ == "__main__":
    test_apis()
