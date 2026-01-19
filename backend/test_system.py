"""
Test Script to Verify Frontend-Backend Connection
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test backend health endpoint"""
    print("\n1. Testing Backend Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_register():
    """Test registration endpoint"""
    print("\n2. Testing Registration...")
    test_email = f"test_{datetime.now().timestamp()}@example.com"
    test_data = {
        "email": test_email,
        "username": f"user_{int(datetime.now().timestamp())}",
        "password": "Test1234!",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            print(f"   User Created: {user_data['email']} (ID: {user_data['id']})")
            return test_data
        else:
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_login(credentials):
    """Test login endpoint"""
    if not credentials:
        print("\n3. Skipping Login (no valid credentials)")
        return None
        
    print("\n3. Testing Login...")
    try:
        # OAuth2 password flow requires form data
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": credentials["username"],
                "password": credentials["password"]
            }
        )
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            login_data = response.json()
            print(f"   Token: {login_data['access_token'][:20]}...")
            print(f"   User: {login_data['user']['email']}")
            return login_data['access_token']
        else:
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with token"""
    if not token:
        print("\n4. Skipping Protected Endpoint (no token)")
        return
        
    print("\n4. Testing Protected Endpoint...")
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   Current User: {user_data['email']}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def check_database():
    """Check database directly"""
    print("\n5. Checking Database...")
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/careerpilot_ai')
        conn = engine.connect()
        
        # Count users
        result = conn.execute(text('SELECT COUNT(*) FROM users'))
        user_count = result.scalar()
        print(f"   ✅ Total users in database: {user_count}")
        
        # Get recent users
        result = conn.execute(text('SELECT email, username, created_at FROM users ORDER BY created_at DESC LIMIT 3'))
        print(f"   Recent users:")
        for row in result:
            print(f"     - {row[0]} ({row[1]}) created at {row[2]}")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("CareerPilot AI - System Test")
    print("=" * 60)
    
    # Run tests
    test_health()
    credentials = test_register()
    token = test_login(credentials)
    test_protected_endpoint(token)
    check_database()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
