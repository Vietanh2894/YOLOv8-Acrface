#!/usr/bin/env python3
"""
FACE RECOGNITION SYSTEM - DEMO HOÀN CHỈNH
"""

import cv2
import os
from face_recognition_system import FaceRecognitionSystem
from insightface.data import get_image as ins_get_image

class FaceRecognitionDemo:
    def __init__(self):
        self.system = FaceRecognitionSystem()
        
    def setup_demo_images(self):
        """Tạo ảnh demo từ InsightFace"""
        print("🎬 Chuẩn bị ảnh demo...")
        
        # Lấy ảnh có nhiều người
        img1 = ins_get_image('t1')  # Ảnh có nhiều khuôn mặt
        cv2.imwrite('demo_group.jpg', img1)
        
        # Cắt từng khuôn mặt để làm ảnh riêng lẻ
        result = self.system.recognize_face('demo_group.jpg')
        if result['success'] and result['total_faces'] > 0:
            for i, match in enumerate(result['matches']):
                x1, y1, x2, y2 = match['bbox']
                face_crop = img1[y1:y2, x1:x2]
                cv2.imwrite(f'person_{i+1}.jpg', face_crop)
        
        print(f"✅ Đã tạo {result['total_faces']} ảnh khuôn mặt riêng lẻ")
        return result['total_faces']
        
    def demo_registration(self):
        """Demo đăng ký khuôn mặt"""
        print("\n" + "="*50)
        print("📝 DEMO: ĐĂNG KÝ KHUÔN MẶT")
        print("="*50)
        
        # Đăng ký 3 người đầu tiên
        people = [
            ("person_1.jpg", "Nguyễn Văn A"),
            ("person_2.jpg", "Trần Thị B"), 
            ("person_3.jpg", "Lê Văn C")
        ]
        
        registered_ids = []
        for img_file, name in people:
            if os.path.exists(img_file):
                print(f"\n📸 Đang đăng ký: {name}")
                result = self.system.register_face(img_file, name)
                
                if result['success']:
                    print(f"✅ Đăng ký thành công! ID: {result['face_id']}")
                    registered_ids.append(result['face_id'])
                else:
                    print(f"❌ Lỗi: {result['message']}")
            else:
                print(f"⚠️ Không tìm thấy file: {img_file}")
        
        return registered_ids
    
    def demo_recognition(self):
        """Demo nhận diện khuôn mặt"""
        print("\n" + "="*50)
        print("🔍 DEMO: NHẬN DIỆN KHUÔN MẶT")
        print("="*50)
        
        print("📸 Nhận diện trong ảnh nhóm...")
        result = self.system.recognize_face('demo_group.jpg')
        
        if result['success']:
            print(f"✅ Phát hiện {result['total_faces']} khuôn mặt:")
            
            for i, match in enumerate(result['matches']):
                print(f"\n--- KHUÔN MẶT {i+1} ---")
                print(f"📍 Vị trí: {match['bbox']}")
                print(f"🎯 Confidence: {match['confidence']:.3f}")
                
                if match['match_found']:
                    print(f"👤 Nhận diện: {match['person_name']}")
                    print(f"🔍 Độ tương tự: {match['match_similarity']:.4f}")
                    print("✅ NHẬN DIỆN THÀNH CÔNG!")
                else:
                    print(f"❓ Chưa nhận diện được")
                    print(f"🔍 Độ tương tự cao nhất: {match['best_similarity']:.4f}")
                    print("⚠️ Người lạ hoặc chưa đăng ký")
        else:
            print(f"❌ Lỗi: {result['message']}")
    
    def demo_comparison(self):
        """Demo so sánh 2 ảnh"""
        print("\n" + "="*50)
        print("⚖️ DEMO: SO SÁNH 2 ẢNH")
        print("="*50)
        
        if os.path.exists('person_1.jpg') and os.path.exists('person_2.jpg'):
            print("📸 So sánh person_1.jpg vs person_2.jpg")
            result = self.system.compare_two_images('person_1.jpg', 'person_2.jpg')
            
            if result['success']:
                print(f"🔍 Độ tương tự: {result['similarity']:.4f}")
                print(f"🎯 Ngưỡng: {result['threshold']}")
                
                if result['is_same_person']:
                    print("✅ CÙNG MỘT NGƯỜI!")
                else:
                    print("❌ KHÁC NGƯỜI!")
            else:
                print(f"❌ Lỗi: {result['message']}")
    
    def show_statistics(self):
        """Hiển thị thống kê"""
        print("\n" + "="*50)
        print("📊 THỐNG KÊ HỆ THỐNG")
        print("="*50)
        
        from database_manager import DatabaseManager
        db = DatabaseManager()
        
        try:
            db.connect()
            embeddings = db.get_all_face_embeddings()
            
            print(f"👥 Tổng số người đã đăng ký: {len(embeddings)}")
            for emb in embeddings:
                print(f"  🆔 ID: {emb['id']} - 👤 Tên: {emb['name']}")
                
        except Exception as e:
            print(f"❌ Lỗi truy vấn database: {e}")
        finally:
            db.close()
    
    def run_complete_demo(self):
        """Chạy demo hoàn chỉnh"""
        try:
            print("🚀 FACE RECOGNITION SYSTEM - DEMO HOÀN CHỈNH")
            print("=" * 60)
            
            # 1. Chuẩn bị ảnh
            total_faces = self.setup_demo_images()
            
            # 2. Demo đăng ký
            registered_ids = self.demo_registration()
            
            # 3. Demo nhận diện
            self.demo_recognition()
            
            # 4. Demo so sánh
            self.demo_comparison()
            
            # 5. Thống kê
            self.show_statistics()
            
            print("\n" + "="*60)
            print("🎉 DEMO HOÀN THÀNH THÀNH CÔNG!")
            print("✅ Hệ thống đã sẵn sàng sử dụng thực tế!")
            print("="*60)
            
            # Hướng dẫn sử dụng
            print("\n📖 HƯỚNG DẪN SỬ DỤNG:")
            print("1. Đăng ký: system.register_face(image_path, person_name)")
            print("2. Nhận diện: system.recognize_face(image_path)")
            print("3. So sánh: system.compare_two_images(img1_path, img2_path)")
            
        except Exception as e:
            print(f"❌ Lỗi trong demo: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.system.close()

if __name__ == "__main__":
    demo = FaceRecognitionDemo()
    demo.run_complete_demo()