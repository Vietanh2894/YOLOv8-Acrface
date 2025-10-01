#!/usr/bin/env python3
"""
Test client để debug compare functionality
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

def test_compare_faces(base_url="http://localhost:8000"):
    """Test compare faces endpoint"""
    
    # Test image paths
    test_images = [
        "test1.jpg",
        "test2.jpg", 
        "test3.jpg",
        "person_1.jpg",
        "person_2.jpg"
    ]
    
    # Find available test images
    available_images = []
    for img in test_images:
        if Path(img).exists():
            available_images.append(img)
    
    if len(available_images) < 2:
        print("❌ Cần ít nhất 2 ảnh để test compare!")
        print(f"Available images: {available_images}")
        return
    
    image1 = available_images[0]
    image2 = available_images[1]
    
    print(f"🖼️ So sánh 2 ảnh:")
    print(f"   Image 1: {image1}")
    print(f"   Image 2: {image2}")
    
    # Convert to base64
    base64_image1 = image_to_base64(image1)
    base64_image2 = image_to_base64(image2)
    
    if not base64_image1 or not base64_image2:
        print("❌ Lỗi convert images to base64")
        return
    
    # Test compare with different thresholds
    thresholds = [0.3, 0.5, 0.6, 0.8]
    
    for threshold in thresholds:
        print(f"\n🔍 Testing compare với threshold = {threshold}...")
        
        compare_data = {
            "image1": base64_image1,
            "image2": base64_image2,
            "threshold": threshold
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/simple-face/compare",
                json=compare_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                
                # Show comparison results
                if result.get('success'):
                    similarity = result.get('similarity')
                    match = result.get('match')
                    
                    if similarity is not None and match is not None:
                        print(f"\n🎯 COMPARISON RESULT (threshold={threshold}):")
                        print(f"   📊 Similarity: {similarity:.4f}")
                        print(f"   ✅ Match: {'YES' if match else 'NO'}")
                        print(f"   🎯 Threshold: {threshold}")
                    else:
                        print(f"\n❌ NULL VALUES:")
                        print(f"   📊 Similarity: {similarity}")
                        print(f"   ✅ Match: {match}")
                else:
                    print(f"\n❌ Compare failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request error: {e}")
        
        print("-" * 50)

def test_health_check(base_url="http://localhost:8000"):
    """Test health check"""
    try:
        response = requests.get(f"{base_url}/api/v1/simple-face/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check: {result['message']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("🧪 FACE COMPARE DEBUG TEST")
    print("=" * 50)
    
    # Test health first
    test_health_check()
    
    # Test compare functionality
    test_compare_faces()
    
    print("\n✅ Test completed!")