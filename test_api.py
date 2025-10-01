#!/usr/bin/env python3
"""
Test script cho Face Recognition API Server
"""

import requests
import base64
import json
import os

# API base URL
API_BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def encode_image_to_base64(image_path):
    """Convert image to base64"""
    try:
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded
    except Exception as e:
        print(f"❌ Error encoding image: {e}")
        return None

def test_register_face():
    """Test face registration"""
    print("\n📝 Testing Face Registration...")
    
    # Sử dụng ảnh mẫu có sẵn
    image_path = "sample_group.jpg"
    if not os.path.exists(image_path):
        print("❌ sample_group.jpg not found!")
        return False
    
    # Encode image
    image_base64 = encode_image_to_base64(image_path)
    if not image_base64:
        return False
    
    # Test data
    data = {
        "name": "API Test User",
        "image": image_base64,
        "description": "Test user from API"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/face/register", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recognize_face():
    """Test face recognition"""
    print("\n🔍 Testing Face Recognition...")
    
    image_path = "sample_group.jpg"
    if not os.path.exists(image_path):
        print("❌ sample_group.jpg not found!")
        return False
    
    image_base64 = encode_image_to_base64(image_path)
    if not image_base64:
        return False
    
    data = {
        "image": image_base64,
        "threshold": 0.6
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/face/recognize", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_compare_faces():
    """Test face comparison"""
    print("\n⚖️ Testing Face Comparison...")
    
    # Sử dụng cùng một ảnh để test
    image_path = "sample_group.jpg"
    if not os.path.exists(image_path):
        print("❌ sample_group.jpg not found!")
        return False
    
    image_base64 = encode_image_to_base64(image_path)
    if not image_base64:
        return False
    
    data = {
        "image1": image_base64,
        "image2": image_base64,  # Cùng ảnh nên similarity cao
        "threshold": 0.6
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/face/compare", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_faces():
    """Test list registered faces"""
    print("\n📊 Testing List Faces...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/face/list")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 FACE RECOGNITION API TESTING")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Face Registration", test_register_face),
        ("Face Recognition", test_recognize_face),
        ("Face Comparison", test_compare_faces),
        ("List Faces", test_list_faces)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        print("✅ PASSED" if success else "❌ FAILED")
    
    print("\n" + "="*50)
    print("📋 TEST RESULTS SUMMARY:")
    print("="*50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API server is working correctly!")
    else:
        print("⚠️ Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()