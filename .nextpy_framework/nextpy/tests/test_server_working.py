#!/usr/bin/env python3
"""Test that the NextPy server is working correctly"""

import requests
import time

def test_server():
    """Test the NextPy development server"""
    
    base_url = "http://localhost:5000"
    
    try:
        print("🧪 Testing NextPy Server...")
        
        # Test homepage
        print("📄 Testing homepage...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Homepage accessible")
            # Check for Tailwind CSS
            if "tailwind" in response.text.lower():
                print("✅ Tailwind CSS is being served")
            else:
                print("⚠️  Tailwind CSS might not be loaded")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
        
        # Test about page
        print("📄 Testing about page...")
        response = requests.get(f"{base_url}/about", timeout=5)
        if response.status_code == 200:
            print("✅ About page accessible")
        else:
            print(f"❌ About page failed: {response.status_code}")
        
        # Test Tailwind CSS file
        print("🎨 Testing Tailwind CSS file...")
        response = requests.get(f"{base_url}/tailwind.css", timeout=5)
        if response.status_code == 200:
            print("✅ Tailwind CSS file accessible")
            # Check for Tailwind classes
            if "flex" in response.text and "text-center" in response.text:
                print("✅ Tailwind classes compiled correctly")
            else:
                print("⚠️  Tailwind classes might be missing")
        else:
            print(f"❌ Tailwind CSS file failed: {response.status_code}")
        
        print("\n🎉 Server test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - make sure it's running on port 5000")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_server()
