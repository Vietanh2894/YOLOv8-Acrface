#!/usr/bin/env python3
"""
SIMPLE DEMO - Face Recognition System
"""

from face_recognition_system import FaceRecognitionSystem
from insightface.data import get_image as ins_get_image
import cv2

def main():
    print("🚀 FACE RECOGNITION SYSTEM - DEMO ĐỊA ĐƠN GIẢN")
    print("="*60)
    
    # Khởi tạo hệ thống
    system = FaceRecognitionSystem()
    
    try:
        # Lấy ảnh mẫu từ InsightFace và lưu
        print("📸 Tải ảnh mẫu từ InsightFace...")
        img = ins_get_image('t1')
        cv2.imwrite('sample_faces.jpg', img)
        print("✅ Đã lưu ảnh: sample_faces.jpg")
        
        # Test nhận diện
        print("\n🔍 Phân tích ảnh...")
        result = system.recognize_face('sample_faces.jpg')
        
        if result['success']:
            print(f"🎉 Tìm thấy {result['total_faces']} khuôn mặt!")
            
            for i, face in enumerate(result['matches'], 1):
                x1, y1, x2, y2 = face['bbox']
                conf = face['confidence']
                print(f"  👤 Khuôn mặt {i}: Tọa độ({x1},{y1},{x2},{y2}) - Confidence: {conf:.3f}")
        else:
            print(f"❌ {result['message']}")
        
        # Thống kê database  
        print(f"\n📊 Database hiện có {system.db_manager.get_total_faces()} người đã đăng ký")
        
        print("\n" + "="*60)
        print("✅ HỆ THỐNG HOẠT ĐỘNG BÌNH THƯỜNG!")
        print("📝 Để sử dụng thực tế:")
        print("  1. Thay 'sample_faces.jpg' bằng ảnh của bạn")
        print("  2. Dùng system.register_face() để đăng ký người mới")
        print("  3. Dùng system.recognize_face() để nhận diện")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        system.close()

if __name__ == "__main__":
    main()