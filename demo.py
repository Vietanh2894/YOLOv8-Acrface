#!/usr/bin/env python3
"""
Demo script for Face Recognition System
Chạy demo hoàn chỉnh của hệ thống nhận diện khuôn mặt
"""

import os
import sys
import time
from pathlib import Path

def print_header():
    print("="*60)
    print("🎯 FACE RECOGNITION SYSTEM DEMO")
    print("🔧 YOLOv8 + InsightFace + MySQL")
    print("="*60)

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết"""
    print("🔍 Kiểm tra requirements...")
    
    missing_modules = []
    
    # Kiểm tra các module cần thiết
    required_modules = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('ultralytics', 'ultralytics'),
        ('insightface', 'insightface'),
        ('pymysql', 'pymysql')
    ]
    
    for module, package in required_modules:
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_modules.append(package)
    
    if missing_modules:
        print(f"\n⚠️ Các module sau chưa được cài đặt: {', '.join(missing_modules)}")
        print("💡 Chạy: python setup.py để cài đặt")
        return False
    
    return True

def create_test_images_if_needed():
    """Tạo ảnh test nếu chưa có"""
    test1 = Path("test3.jpg")
    test2 = Path("test4.jpg")
    
    if not test1.exists() or not test2.exists():
        print("🖼️ Tạo ảnh test...")
        try:
            from create_test_images import create_test_image
            if not test1.exists():
                create_test_image("test3.jpg", "Person 3")
            if not test2.exists():
                create_test_image("test4.jpg", "Person 4")
            print("✅ Đã tạo ảnh test")
        except Exception as e:
            print(f"❌ Lỗi tạo ảnh test: {e}")
            return False
    
    return True

def test_database_connection():
    """Test kết nối database"""
    print("🗄️ Kiểm tra kết nối database...")
    
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager()
        db.close()
        print("✅ Kết nối database thành công")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        print("💡 Kiểm tra:")
        print("   - MySQL server đang chạy?")
        print("   - Cấu hình trong config.py đúng?")
        print("   - Database 'smartparking' đã tồn tại?")
        return False

def run_face_recognition_demo():
    """Chạy demo nhận diện khuôn mặt"""
    print("🚀 Bắt đầu demo Face Recognition...")
    
    try:
        from face_recognition_system import FaceRecognitionSystem
        
        # Khởi tạo hệ thống
        system = FaceRecognitionSystem()
        
        # Demo 1: Đăng ký khuôn mặt
        print("\n📝 DEMO 1: Đăng ký khuôn mặt")
        print("-" * 30)

        if os.path.exists("test3.jpg"):
            result = system.register_face("test3.jpg", "Demo Person 3")
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"📊 Face ID: {result['face_id']}")
                print(f"🎯 Confidence: {result['confidence']:.3f}")
            else:
                print(f"❌ {result['message']}")
        
        # Demo 2: Nhận diện khuôn mặt
        print("\n🔍 DEMO 2: Nhận diện khuôn mặt")
        print("-" * 30)

        if os.path.exists("test4.jpg"):
            result = system.recognize_face("test4.jpg")
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"👥 Số khuôn mặt: {result['total_faces']}")
                
                for i, match in enumerate(result['matches']):
                    print(f"\n--- Khuôn mặt {i+1} ---")
                    if match['match_found']:
                        print(f"👤 Người: {match['person_name']}")
                        print(f"🎯 Similarity: {match['match_similarity']:.4f}")
                        print(f"✅ Nhận diện: THÀNH CÔNG")
                    else:
                        print(f"👤 Người: {match['person_name']}")
                        print(f"🎯 Best similarity: {match['best_similarity']:.4f}")
                        print(f"❌ Nhận diện: KHÔNG THÀNH CÔNG")
            else:
                print(f"❌ {result['message']}")
        
        # Demo 3: So sánh 2 ảnh
        print("\n⚖️ DEMO 3: So sánh 2 ảnh")
        print("-" * 30)
        
        if os.path.exists("test3.jpg") and os.path.exists("test4.jpg"):
            result = system.compare_two_images("test3.jpg", "test4.jpg")
            if result['success']:
                print(f"✅ {result['message']}")
                comp = result['comparison']
                print(f"🔍 Similarity: {comp['similarity']:.4f}")
                print(f"🎯 Threshold: {comp['threshold']:.4f}")
                print(f"👥 Cùng người: {'CÓ' if comp['is_same_person'] else 'KHÔNG'}")
                print(f"📊 Confidence: {comp['confidence']:.4f}")
            else:
                print(f"❌ {result['message']}")
        
        system.close()
        print("\n🎉 Demo hoàn thành!")
        
    except Exception as e:
        print(f"❌ Lỗi chạy demo: {e}")
        import traceback
        traceback.print_exc()

def main():
    print_header()
    
    # Bước 1: Kiểm tra requirements
    if not check_requirements():
        return False
    
    time.sleep(1)
    
    # Bước 2: Tạo ảnh test
    if not create_test_images_if_needed():
        return False
    
    time.sleep(1)
    
    # Bước 3: Test database
    if not test_database_connection():
        return False
    
    time.sleep(1)
    
    # Bước 4: Chạy demo
    run_face_recognition_demo()
    
    print("\n" + "="*60)
    print("✅ DEMO HOÀN TẤT!")
    print("📖 Đọc README_face_recognition.md để biết thêm chi tiết")
    print("🔧 Tùy chỉnh config.py để điều chỉnh hệ thống")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Đã dừng demo bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)