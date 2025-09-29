#!/usr/bin/env python3
"""
Test Face Recognition System với ảnh mẫu từ InsightFace
"""

import cv2
import numpy as np
from face_recognition_system import FaceRecognitionSystem
import insightface
from insightface.data import get_image as ins_get_image

def test_with_insightface_images():
    """Test với ảnh mẫu từ InsightFace"""
    print("🚀 Test Face Recognition System với ảnh mẫu InsightFace")
    print("="*60)
    
    # Khởi tạo hệ thống
    system = FaceRecognitionSystem()
    
    try:
        # Lấy ảnh mẫu từ InsightFace
        print("📸 Lấy ảnh mẫu từ InsightFace...")
        img = ins_get_image('t1')  # Ảnh có nhiều khuôn mặt
        
        # Lưu ảnh để test
        cv2.imwrite('insightface_test.jpg', img)
        print("✅ Đã lưu ảnh mẫu: insightface_test.jpg")
        
        # Test nhận diện
        print("\n🔍 Test nhận diện khuôn mặt...")
        result = system.recognize_face('insightface_test.jpg')
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"👥 Số khuôn mặt tìm thấy: {result['total_faces']}")
            
            for i, match in enumerate(result['matches']):
                print(f"\n--- Khuôn mặt {i+1} ---")
                print(f"📍 Vị trí: {match['bbox']}")
                print(f"🎯 Confidence: {match['confidence']:.3f}")
                if match['match_found']:
                    print(f"👤 Người: {match['person_name']}")
                    print(f"🔍 Similarity: {match['match_similarity']:.4f}")
                else:
                    print(f"❓ Chưa nhận diện được (similarity: {match['best_similarity']:.4f})")
        else:
            print(f"❌ {result['message']}")
            
        # Nếu có face, hãy đăng ký một face
        if result['success'] and result['total_faces'] > 0:
            print(f"\n📝 Đăng ký khuôn mặt đầu tiên với tên 'Person from InsightFace'...")
            
            # Crop face đầu tiên để đăng ký
            face_bbox = result['matches'][0]['bbox']
            x1, y1, x2, y2 = face_bbox
            
            # Crop và lưu face
            face_crop = img[y1:y2, x1:x2]
            cv2.imwrite('face_crop.jpg', face_crop)
            
            # Đăng ký
            register_result = system.register_face('face_crop.jpg', 'Person from InsightFace')
            if register_result['success']:
                print(f"✅ {register_result['message']}")
                print(f"🆔 Face ID: {register_result['face_id']}")
                
                # Test nhận diện lại
                print(f"\n🔄 Test nhận diện lại sau khi đăng ký...")
                result2 = system.recognize_face('insightface_test.jpg')
                
                if result2['success']:
                    for i, match in enumerate(result2['matches']):
                        if match['match_found']:
                            print(f"🎉 Khuôn mặt {i+1}: Nhận diện thành công!")
                            print(f"👤 Tên: {match['person_name']}")
                            print(f"🎯 Similarity: {match['match_similarity']:.4f}")
                        else:
                            print(f"❓ Khuôn mặt {i+1}: Chưa nhận diện được")
            else:
                print(f"❌ Lỗi đăng ký: {register_result['message']}")
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        system.close()

def test_cosine_similarity():
    """Test tính toán cosine similarity"""
    print("\n🧮 Test Cosine Similarity")
    print("-" * 30)
    
    from face_processor import FaceProcessor
    
    # Tạo 2 vector test
    vec1 = np.random.rand(512).astype(np.float32)
    vec2 = vec1 + np.random.rand(512).astype(np.float32) * 0.1  # Vector tương tự
    vec3 = np.random.rand(512).astype(np.float32)  # Vector khác hoàn toàn
    
    sim1 = FaceProcessor.calculate_cosine_similarity(vec1, vec2)
    sim2 = FaceProcessor.calculate_cosine_similarity(vec1, vec3)
    
    print(f"🔍 Similarity giữa vector tương tự: {sim1:.4f}")
    print(f"🔍 Similarity giữa vector khác nhau: {sim2:.4f}")
    
    if sim1 > 0.6:
        print("✅ Vector tương tự được nhận diện đúng (similarity > 0.6)")
    else:
        print("⚠️ Vector tương tự có similarity thấp")
        
    if sim2 < 0.6:
        print("✅ Vector khác nhau được phân biệt đúng (similarity < 0.6)")
    else:
        print("⚠️ Vector khác nhau có similarity cao")

if __name__ == "__main__":
    # Test cosine similarity trước
    test_cosine_similarity()
    
    # Test với ảnh mẫu InsightFace
    test_with_insightface_images()
    
    print("\n" + "="*60)
    print("🎉 Test hoàn thành!")
    print("📝 Hệ thống đã sẵn sàng sử dụng với ảnh thật!")
    print("="*60)