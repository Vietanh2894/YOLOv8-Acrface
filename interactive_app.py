#!/usr/bin/env python3
"""
🎮 FACE RECOGNITION - ỨNG DỤNG TƯƠNG TÁC
"""

from face_recognition_system import FaceRecognitionSystem
import os
from insightface.data import get_image as ins_get_image
import cv2

class InteractiveFaceApp:
    def __init__(self):
        print("🚀 Khởi động Face Recognition System...")
        self.system = FaceRecognitionSystem()
        self.setup_sample_images()
        
    def setup_sample_images(self):
        """Tạo ảnh mẫu để user có thể test ngay"""
        print("📸 Chuẩn bị ảnh mẫu...")
        
        # Tạo ảnh nhóm mẫu
        img = ins_get_image('t1')
        cv2.imwrite('sample_group.jpg', img)
        
        # Tạo thư mục demo
        if not os.path.exists('demo_images'):
            os.makedirs('demo_images')
            
        print("✅ Đã chuẩn bị ảnh mẫu: sample_group.jpg")
        
    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*60)
        print("🎯 FACE RECOGNITION SYSTEM - MENU")
        print("="*60)
        print("1. 📝 Đăng ký khuôn mặt mới")
        print("2. 🔍 Nhận diện khuôn mặt trong ảnh")  
        print("3. ⚖️ So sánh hai ảnh")
        print("4. 📊 Xem danh sách đã đăng ký")
        print("5. 🧪 Test với ảnh mẫu InsightFace")
        print("6. ⚙️ Điều chỉnh cấu hình")
        print("7. 🆘 Hướng dẫn sử dụng")
        print("0. ❌ Thoát")
        print("="*60)
        
    def register_face_menu(self):
        """Menu đăng ký khuôn mặt"""
        print("\n📝 ĐĂNG KÝ KHUÔN MẶT MỚI")
        print("-" * 30)
        
        print("Lựa chọn:")
        print("1. Nhập đường dẫn ảnh")
        print("2. Sử dụng ảnh mẫu (sample_group.jpg)")
        print("0. Quay lại")
        
        choice = input("Chọn (0-2): ").strip()
        
        if choice == "1":
            img_path = input("Nhập đường dẫn ảnh: ").strip()
            if not os.path.exists(img_path):
                print("❌ File không tồn tại!")
                return
        elif choice == "2":
            img_path = "sample_group.jpg"
            print("📸 Sử dụng ảnh mẫu")
        elif choice == "0":
            return
        else:
            print("❌ Lựa chọn không hợp lệ!")
            return
            
        name = input("Nhập tên người: ").strip()
        if not name:
            print("❌ Tên không được để trống!")
            return
            
        print(f"⏳ Đang xử lý ảnh {img_path}...")
        result = self.system.register_face(img_path, name)
        
        if result['success']:
            print(f"✅ Đăng ký thành công!")
            print(f"🆔 Face ID: {result['face_id']}")
            print(f"👤 Tên: {result['person_name']}")
        else:
            print(f"❌ Lỗi: {result['message']}")
            print("💡 Gợi ý: Hãy thử ảnh khác có khuôn mặt rõ nét hơn")
            
    def recognize_face_menu(self):
        """Menu nhận diện khuôn mặt"""
        print("\n🔍 NHẬN DIỆN KHUÔN MẶT")
        print("-" * 30)
        
        print("Lựa chọn:")
        print("1. Nhập đường dẫn ảnh")
        print("2. Sử dụng ảnh mẫu (sample_group.jpg)")
        print("0. Quay lại")
        
        choice = input("Chọn (0-2): ").strip()
        
        if choice == "1":
            img_path = input("Nhập đường dẫn ảnh: ").strip()
            if not os.path.exists(img_path):
                print("❌ File không tồn tại!")
                return
        elif choice == "2":
            img_path = "sample_group.jpg"
            print("📸 Sử dụng ảnh mẫu")
        elif choice == "0":
            return
        else:
            print("❌ Lựa chọn không hợp lệ!")
            return
            
        print(f"⏳ Đang phân tích ảnh {img_path}...")
        result = self.system.recognize_face(img_path)
        
        if result['success']:
            print(f"🎉 Tìm thấy {result['total_faces']} khuôn mặt:")
            
            for i, match in enumerate(result['matches'], 1):
                print(f"\n--- KHUÔN MẶT {i} ---")
                x1, y1, x2, y2 = match['bbox']
                print(f"📍 Vị trí: ({x1},{y1}) → ({x2},{y2})")
                print(f"🎯 Confidence: {match['confidence']:.3f}")
                
                if match['match_found']:
                    print(f"👤 Nhận diện: {match['person_name']}")
                    print(f"🔍 Độ tương tự: {match['match_similarity']:.4f}")
                    print("✅ NHẬN DIỆN THÀNH CÔNG!")
                else:
                    print(f"❓ Người lạ")
                    print(f"🔍 Độ tương tự cao nhất: {match['best_similarity']:.4f}")
                    print("⚠️ Chưa đăng ký hoặc similarity thấp")
        else:
            print(f"❌ {result['message']}")
            
    def compare_images_menu(self):
        """Menu so sánh ảnh"""
        print("\n⚖️ SO SÁNH HAI ẢNH")
        print("-" * 30)
        
        img1 = input("Ảnh thứ nhất: ").strip()
        img2 = input("Ảnh thứ hai: ").strip()
        
        if not os.path.exists(img1):
            print(f"❌ File {img1} không tồn tại!")
            return
        if not os.path.exists(img2):
            print(f"❌ File {img2} không tồn tại!")
            return
            
        print("⏳ Đang so sánh...")
        result = self.system.compare_two_images(img1, img2)
        
        if result['success']:
            comparison = result['comparison']
            print(f"🔍 Độ tương tự: {comparison['similarity']:.4f}")
            print(f"🎯 Ngưỡng: {comparison['threshold']}")
            
            if comparison['is_same_person']:
                print("✅ KẾT LUẬN: CÙNG MỘT NGƯỜI!")
            else:
                print("❌ KẾT LUẬN: KHÁC NGƯỜI!")
                
            # Gợi ý
            similarity = comparison['similarity']
            if similarity > 0.9:
                print("💡 Độ tương tự rất cao - chắc chắn cùng người")
            elif similarity > 0.7:
                print("💡 Độ tương tự cao - có thể cùng người")
            elif similarity > 0.5:
                print("💡 Độ tương tự trung bình - cần xem xét thêm")
            else:
                print("💡 Độ tương tự thấp - khác người")
        else:
            print(f"❌ {result['message']}")
            
    def show_registered_list(self):
        """Hiển thị danh sách đã đăng ký"""
        print("\n📊 DANH SÁCH KHUÔN MẶT ĐÃ ĐĂNG KÝ")
        print("-" * 40)
        
        try:
            total = self.system.db_manager.get_total_faces()
            print(f"👥 Tổng số người đã đăng ký: {total}")
            
            if total > 0:
                embeddings = self.system.db_manager.get_all_face_embeddings()
                print("\nChi tiết:")
                for i, emb in enumerate(embeddings, 1):
                    print(f"  {i:2d}. 🆔 ID: {emb['id']:3d} | 👤 {emb['name']}")
            else:
                print("📝 Chưa có ai được đăng ký. Hãy đăng ký người đầu tiên!")
                
        except Exception as e:
            print(f"❌ Lỗi truy vấn database: {e}")
            
    def test_sample_images(self):
        """Test với ảnh mẫu InsightFace"""
        print("\n🧪 TEST VỚI ẢNH MẪU INSIGHTFACE")
        print("-" * 40)
        
        print("⏳ Đang phân tích ảnh mẫu...")
        result = self.system.recognize_face('sample_group.jpg')
        
        if result['success']:
            print(f"✅ Phát hiện thành công {result['total_faces']} khuôn mặt!")
            print(f"📊 Chi tiết:")
            
            for i, match in enumerate(result['matches'], 1):
                conf = match['confidence']
                print(f"  👤 Khuôn mặt {i}: Confidence = {conf:.3f}")
                
            print(f"\n💡 Kết quả:")
            print(f"   • YOLOv8 hoạt động: ✅")
            print(f"   • InsightFace hoạt động: ✅")  
            print(f"   • Database kết nối: ✅")
            print(f"   • Hệ thống sẵn sàng sử dụng: ✅")
        else:
            print(f"❌ {result['message']}")
            
    def config_menu(self):
        """Menu cấu hình"""
        print("\n⚙️ ĐIỀU CHỈNH CẤU HÌNH")
        print("-" * 30)
        
        current_threshold = self.system.face_processor.face_similarity_threshold
        print(f"🎯 Ngưỡng similarity hiện tại: {current_threshold}")
        
        print("\nLựa chọn:")
        print("1. Thay đổi ngưỡng similarity")
        print("2. Xem thông tin hệ thống")
        print("0. Quay lại")
        
        choice = input("Chọn (0-2): ").strip()
        
        if choice == "1":
            try:
                new_threshold = float(input("Nhập ngưỡng mới (0.0-1.0): "))
                if 0.0 <= new_threshold <= 1.0:
                    self.system.face_processor.face_similarity_threshold = new_threshold
                    print(f"✅ Đã cập nhật ngưỡng: {new_threshold}")
                    
                    if new_threshold < 0.5:
                        print("⚠️ Ngưỡng thấp - có thể nhận diện sai")
                    elif new_threshold > 0.8:
                        print("⚠️ Ngưỡng cao - có thể bỏ sót người quen")
                else:
                    print("❌ Ngưỡng phải từ 0.0 đến 1.0")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ")
                
        elif choice == "2":
            self.show_system_info()
            
    def show_system_info(self):
        """Hiển thị thông tin hệ thống"""
        print("\n📋 THÔNG TIN HỆ THỐNG")
        print("-" * 30)
        print("🤖 YOLOv8: Phát hiện khuôn mặt")
        print("🧠 InsightFace Buffalo_L: Trích xuất embedding 512D")
        print("💾 MySQL: Lưu trữ embedding")
        print("📐 Cosine Similarity: So sánh độ tương tự")
        print(f"🎯 Ngưỡng hiện tại: {self.system.face_processor.face_similarity_threshold}")
        
        try:
            total = self.system.db_manager.get_total_faces()
            print(f"👥 Người đã đăng ký: {total}")
        except:
            print("👥 Người đã đăng ký: Không thể truy cập DB")
            
    def show_help(self):
        """Hiển thị hướng dẫn"""
        print("\n🆘 HƯỚNG DẪN SỬ DỤNG NHANH")
        print("-" * 40)
        print("1. 📝 Đăng ký: Chọn 1 → Chọn ảnh → Nhập tên")
        print("2. 🔍 Nhận diện: Chọn 2 → Chọn ảnh")
        print("3. ⚖️ So sánh: Chọn 3 → Nhập 2 đường dẫn ảnh")
        print("4. 🧪 Test: Chọn 5 để test hệ thống")
        print("")
        print("💡 TIPS:")
        print("• Ảnh nên rõ nét, khuôn mặt ít nhất 100x100 pixels")
        print("• Ngưỡng 0.6 phù hợp cho hầu hết trường hợp")
        print("• File sample_group.jpg có sẵn để test")
        print("• Đọc file HUONG_DAN_SU_DUNG.md để biết chi tiết")
        
    def run(self):
        """Chạy ứng dụng chính"""
        try:
            print("✅ Hệ thống đã sẵn sàng!")
            
            while True:
                self.show_menu()
                choice = input("\nChọn chức năng (0-7): ").strip()
                
                if choice == "1":
                    self.register_face_menu()
                elif choice == "2":
                    self.recognize_face_menu()
                elif choice == "3":
                    self.compare_images_menu()
                elif choice == "4":
                    self.show_registered_list()
                elif choice == "5":
                    self.test_sample_images()
                elif choice == "6":
                    self.config_menu()
                elif choice == "7":
                    self.show_help()
                elif choice == "0":
                    print("\n👋 Tạm biệt! Cảm ơn bạn đã sử dụng!")
                    break
                else:
                    print("❌ Lựa chọn không hợp lệ! Vui lòng chọn 0-7")
                    
                input("\n⏎ Nhấn Enter để tiếp tục...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
        except Exception as e:
            print(f"\n❌ Lỗi hệ thống: {e}")
        finally:
            self.system.close()

if __name__ == "__main__":
    print("🎮 FACE RECOGNITION - ỨNG DỤNG TƯƠNG TÁC")
    print("=" * 60)
    
    app = InteractiveFaceApp()
    app.run()