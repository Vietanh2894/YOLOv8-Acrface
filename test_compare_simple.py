#!/usr/bin/env python3
"""
Simple test for compare functionality - debug version
"""

import base64
import json
from face_recognition_system import FaceRecognitionSystem

def test_compare_direct():
    """Test compare functionality directly without API"""
    print("🧪 TESTING COMPARE FUNCTIONALITY DIRECTLY")
    print("=" * 50)
    
    # Initialize system
    face_system = FaceRecognitionSystem()
    
    # Test với 2 ảnh có sẵn
    test_images = ["test1.jpg", "test2.jpg", "person_1.jpg", "person_2.jpg"]
    
    available_images = []
    import os
    for img in test_images:
        if os.path.exists(img):
            available_images.append(img)
    
    if len(available_images) < 2:
        print(f"❌ Cần ít nhất 2 ảnh. Available: {available_images}")
        return
    
    image1 = available_images[0]
    image2 = available_images[1]
    
    print(f"🖼️ So sánh 2 ảnh:")
    print(f"   Image 1: {image1}")
    print(f"   Image 2: {image2}")
    
    # Convert to base64
    def image_to_base64(image_path):
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    
    try:
        base64_image1 = image_to_base64(image1)
        base64_image2 = image_to_base64(image2)
        
        print(f"✅ Converted images to base64")
        
        # Test compare with different thresholds
        thresholds = [0.3, 0.6, 0.8]
        
        for threshold in thresholds:
            print(f"\n🔍 Testing với threshold = {threshold}...")
            
            result = face_system.compare_faces_from_base64(
                base64_image1=base64_image1,
                base64_image2=base64_image2,
                threshold=threshold
            )
            
            print(f"📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            if result.get('success'):
                similarity = result.get('similarity')
                match = result.get('match')
                
                if similarity is not None and match is not None:
                    print(f"\n✅ COMPARISON SUCCESS:")
                    print(f"   📊 Similarity: {similarity:.4f}")
                    print(f"   🎯 Match: {'YES' if match else 'NO'}")
                    print(f"   🎯 Threshold: {threshold}")
                else:
                    print(f"\n❌ NULL VALUES DETECTED:")
                    print(f"   📊 Similarity: {similarity}")
                    print(f"   🎯 Match: {match}")
            else:
                print(f"\n❌ COMPARISON FAILED:")
                print(f"   Message: {result.get('message', 'Unknown error')}")
            
            print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        face_system.close()

if __name__ == "__main__":
    test_compare_direct()
    print("\n✅ Test completed!")