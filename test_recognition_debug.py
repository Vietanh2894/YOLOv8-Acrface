#!/usr/bin/env python3
"""
Test client để debug recognition functionality
"""

import requests
import json
import base64
from pathlib import Path

def image_to_base64(image_path):
    """Convert image file to base64"""
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

def test_recognition(base_url="http://localhost:8000"):
    """Test recognition endpoint with debug info"""
    
    # Test image paths
    test_images = [
        "test1.png",
        "test2.png", 
        "test.jpg"
    ]
    
    # Find available test image
    test_image = None
    for img in test_images:
        if Path(img).exists():
            test_image = img
            break
    
    if not test_image:
        print("❌ Không tìm thấy ảnh test nào!")
        return
    
    print(f"🖼️ Sử dụng ảnh test: {test_image}")
    
    # Convert to base64
    base64_image = image_to_base64(test_image)
    if not base64_image:
        return
    
    # Test recognition
    recognition_data = {
        "image": base64_image,
        "threshold": 0.3  # Lower threshold for testing
    }
    
    print(f"\n🔍 Testing recognition với threshold = 0.3...")
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/simple-face/recognize",
            json=recognition_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Show recognition results
            if result.get('success'):
                if result.get('name'):
                    print(f"\n🎯 FOUND MATCH:")
                    print(f"   👤 Name: {result['name']}")
                    print(f"   🆔 Face ID: {result['face_id']}")
                    print(f"   📊 Similarity: {result['similarity']:.4f}")
                    print(f"   💪 Confidence: {result.get('confidence', 'N/A')}")
                else:
                    print(f"\n❌ NO MATCH:")
                    print(f"   📊 Best Similarity: {result['similarity']:.4f}")
                    print(f"   🎯 Threshold: 0.3")
            else:
                print(f"\n❌ Recognition failed: {result['message']}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")

def test_database_list(base_url="http://localhost:8000"):
    """List all faces in database"""
    try:
        response = requests.get(f"{base_url}/api/v1/simple-face/list")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📊 Database info:")
            print(f"   Total faces: {result.get('total', 0)}")
            
            if result.get('faces'):
                for face in result['faces']:
                    print(f"   • ID: {face['id']}, Name: {face['name']}, Description: {face.get('description', 'None')}")
            else:
                print("   🔍 Database is empty")
        else:
            print(f"❌ Error listing faces: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 FACE RECOGNITION DEBUG TEST")
    print("=" * 50)
    
    # Test database first
    test_database_list()
    
    # Test recognition
    test_recognition()
    
    print("\n✅ Test completed!")