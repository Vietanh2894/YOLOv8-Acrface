#!/usr/bin/env python3
"""
🚀 QUICK START - Face Recognition System
Chạy ngay để trải nghiệm hệ thống!
"""

from face_recognition_system import FaceRecognitionSystem
from insightface.data import get_image as ins_get_image
import cv2

def quick_demo():
    """Demo nhanh trong 30 giây"""
    print("🚀 FACE RECOGNITION - QUICK START DEMO")
    print("=" * 50)
    
    # 1. Khởi tạo hệ thống
    print("⏳ 1/4 - Khởi tạo hệ thống...")
    system = FaceRecognitionSystem()
    
    # 2. Tạo ảnh test
    print("⏳ 2/4 - Chuẩn bị ảnh test...")
    img = ins_get_image('t1')
    cv2.imwrite('test1.jpg', img)
    
    # 3. Nhận diện trong ảnh (chưa đăng ký ai)
    print("⏳ 3/4 - Test nhận diện (database trống)...")
    result = system.recognize_face('test1.jpg')
    
    if result['success']:
        print(f"✅ Tìm thấy {result['total_faces']} khuôn mặt!")
        print("📝 Tất cả đều là 'người lạ' vì chưa đăng ký ai")
    
    # 4. Thống kê
    print("⏳ 4/4 - Thống kê hệ thống...")
    total_registered = system.db_manager.get_total_faces()
    print(f"👥 Số người đã đăng ký: {total_registered}")
    
    # Kết thúc
    system.close()
    print("\n" + "=" * 50)
    print("🎉 DEMO HOÀN THÀNH!")
    print("✅ Hệ thống hoạt động bình thường!")
    print("📝 Để sử dụng đầy đủ, chạy: python interactive_app.py")
    print("=" * 50)

def show_usage_summary():
    """Hiển thị tóm tắt cách sử dụng"""
    print("\n📖 TÓM TẮT CÁCH SỬ DỤNG")
    print("-" * 30)
    print("🎮 Ứng dụng tương tác:  python interactive_app.py")
    print("🧪 Demo đơn giản:       python simple_demo.py")  
    print("🚀 Quick start:         python quickstart.py")
    print("📝 Đọc hướng dẫn:       HUONG_DAN_SU_DUNG.md")
    
    print("\n⚡ SỬ DỤNG TRONG CODE:")
    print("""
from face_recognition_system import FaceRecognitionSystem

# Khởi tạo
system = FaceRecognitionSystem()

# Đăng ký 
result = system.register_face("path/to/image.jpg", "Tên người")

# Nhận diện
result = system.recognize_face("path/to/group.jpg")

# So sánh
result = system.compare_two_images("img1.jpg", "img2.jpg")

# Đóng
system.close()
    """)
    
    print("💡 FILE QUAN TRỌNG:")
    print("• config.py - Cấu hình database, threshold")
    print("• sample_group.jpg - Ảnh test có sẵn")
    print("• HUONG_DAN_SU_DUNG.md - Hướng dẫn chi tiết")

if __name__ == "__main__":
    try:
        quick_demo()
        show_usage_summary()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("💡 Hãy kiểm tra:")
        print("   • MySQL đã chạy chưa?")
        print("   • Config database trong config.py đúng chưa?")
        print("   • Đã cài đặt packages chưa? (python setup.py)")