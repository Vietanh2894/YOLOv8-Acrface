# 📖 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG FACE RECOGNITION

## 🚀 Bước 1: Khởi động hệ thống

### Cách 1: Chạy demo nhanh
```bash
python simple_demo.py
```
Demo này sẽ:
- Tải ảnh mẫu từ InsightFace
- Phát hiện và đếm số khuôn mặt
- Hiển thị tọa độ và confidence của từng khuôn mặt

### Cách 2: Sử dụng trong code Python
```python
from face_recognition_system import FaceRecognitionSystem

# Khởi tạo hệ thống
system = FaceRecognitionSystem()
```

## 📝 Bước 2: Đăng ký khuôn mặt mới

### 2.1. Chuẩn bị ảnh
- Ảnh có độ phân giải tốt (tối thiểu 640x480)
- Khuôn mặt rõ nét, không bị che khuất
- Ánh sáng đủ, không quá tối hoặc quá sáng
- Format: JPG, PNG, BMP

### 2.2. Đăng ký trong code
```python
# Đăng ký một người
result = system.register_face("path/to/person1.jpg", "Nguyễn Văn A")

if result['success']:
    print(f"✅ Đăng ký thành công!")
    print(f"🆔 Face ID: {result['face_id']}")
    print(f"👤 Tên: {result['person_name']}")
else:
    print(f"❌ Lỗi: {result['message']}")
```

### 2.3. Đăng ký nhiều người
```python
people_data = [
    ("photos/john.jpg", "John Doe"),
    ("photos/mary.jpg", "Mary Smith"),
    ("photos/peter.jpg", "Peter Johnson")
]

for img_path, name in people_data:
    result = system.register_face(img_path, name)
    print(f"Đăng ký {name}: {'✅' if result['success'] else '❌'}")
```

## 🔍 Bước 3: Nhận diện khuôn mặt

### 3.1. Nhận diện từ ảnh có nhiều người
```python
# Nhận diện trong ảnh nhóm
result = system.recognize_face("group_photo.jpg")

if result['success']:
    print(f"🎉 Tìm thấy {result['total_faces']} khuôn mặt:")
    
    for i, match in enumerate(result['matches'], 1):
        print(f"\n--- KHUÔN MẶT {i} ---")
        print(f"📍 Vị trí: {match['bbox']}")
        print(f"🎯 Confidence: {match['confidence']:.3f}")
        
        if match['match_found']:
            print(f"👤 Tên: {match['person_name']}")
            print(f"🔍 Độ tương tự: {match['match_similarity']:.4f}")
            print("✅ NHẬN DIỆN THÀNH CÔNG!")
        else:
            print(f"❓ Người lạ (similarity: {match['best_similarity']:.4f})")
```

### 3.2. Nhận diện với ngưỡng tùy chỉnh
```python
# Thay đổi ngưỡng similarity (mặc định 0.6)
system.face_processor.face_similarity_threshold = 0.7  # Strict hơn
# hoặc
system.face_processor.face_similarity_threshold = 0.5  # Loose hơn

result = system.recognize_face("test_image.jpg")
```

## ⚖️ Bước 4: So sánh hai ảnh

```python
# So sánh 2 ảnh để xem có phải cùng một người không
result = system.compare_two_images("person1_photo1.jpg", "person1_photo2.jpg")

if result['success']:
    print(f"🔍 Độ tương tự: {result['similarity']:.4f}")
    print(f"🎯 Ngưỡng: {result['threshold']}")
    
    if result['is_same_person']:
        print("✅ CÙNG MỘT NGƯỜI!")
    else:
        print("❌ KHÁC NGƯỜI!")
```

## 🎮 Bước 5: Tạo ứng dụng hoàn chỉnh

Tạo file `my_face_app.py`:

```python
#!/usr/bin/env python3
from face_recognition_system import FaceRecognitionSystem
import os

def main():
    system = FaceRecognitionSystem()
    
    while True:
        print("\n" + "="*50)
        print("🎯 FACE RECOGNITION SYSTEM")
        print("="*50)
        print("1. 📝 Đăng ký khuôn mặt mới")
        print("2. 🔍 Nhận diện khuôn mặt")
        print("3. ⚖️ So sánh 2 ảnh")
        print("4. 📊 Xem danh sách đã đăng ký")
        print("0. ❌ Thoát")
        
        choice = input("\nChọn chức năng (0-4): ").strip()
        
        if choice == "1":
            register_new_face(system)
        elif choice == "2":
            recognize_faces(system)
        elif choice == "3":
            compare_images(system)
        elif choice == "4":
            show_registered_faces(system)
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")
    
    system.close()

def register_new_face(system):
    print("\n📝 ĐĂNG KÝ KHUÔN MẶT MỚI")
    
    img_path = input("Nhập đường dẫn ảnh: ").strip()
    if not os.path.exists(img_path):
        print("❌ File không tồn tại!")
        return
    
    name = input("Nhập tên người: ").strip()
    if not name:
        print("❌ Tên không được để trống!")
        return
    
    result = system.register_face(img_path, name)
    
    if result['success']:
        print(f"✅ Đăng ký thành công! ID: {result['face_id']}")
    else:
        print(f"❌ Lỗi: {result['message']}")

def recognize_faces(system):
    print("\n🔍 NHẬN DIỆN KHUÔN MẶT")
    
    img_path = input("Nhập đường dẫn ảnh: ").strip()
    if not os.path.exists(img_path):
        print("❌ File không tồn tại!")
        return
    
    result = system.recognize_face(img_path)
    
    if result['success']:
        print(f"🎉 Tìm thấy {result['total_faces']} khuôn mặt:")
        
        for i, match in enumerate(result['matches'], 1):
            print(f"\n--- Khuôn mặt {i} ---")
            if match['match_found']:
                print(f"👤 {match['person_name']} ({match['match_similarity']:.3f})")
            else:
                print(f"❓ Người lạ ({match['best_similarity']:.3f})")
    else:
        print(f"❌ {result['message']}")

def compare_images(system):
    print("\n⚖️ SO SÁNH HAI ẢNH")
    
    img1 = input("Ảnh thứ nhất: ").strip()
    img2 = input("Ảnh thứ hai: ").strip()
    
    if not os.path.exists(img1) or not os.path.exists(img2):
        print("❌ Một trong hai file không tồn tại!")
        return
    
    result = system.compare_two_images(img1, img2)
    
    if result['success']:
        print(f"🔍 Độ tương tự: {result['similarity']:.4f}")
        if result['is_same_person']:
            print("✅ CÙNG MỘT NGƯỜI!")
        else:
            print("❌ KHÁC NGƯỜI!")
    else:
        print(f"❌ {result['message']}")

def show_registered_faces(system):
    print("\n📊 DANH SÁCH ĐÃ ĐĂNG KÝ")
    
    total = system.db_manager.get_total_faces()
    print(f"👥 Tổng số: {total} người")
    
    if total > 0:
        embeddings = system.db_manager.get_all_face_embeddings()
        for emb in embeddings:
            print(f"  🆔 {emb['id']}: {emb['name']}")

if __name__ == "__main__":
    main()
```

## 📊 Bước 6: Theo dõi và debugging

### 6.1. Kiểm tra database
```python
from database_manager import DatabaseManager

db = DatabaseManager()
db.connect()

# Xem tổng số người đã đăng ký
total = db.get_total_faces()
print(f"Tổng số: {total}")

# Xem chi tiết
faces = db.get_all_face_embeddings()
for face in faces:
    print(f"ID: {face['id']}, Tên: {face['name']}")

db.close()
```

### 6.2. Test chất lượng ảnh
```python
# Kiểm tra ảnh có phù hợp không
from face_processor import FaceProcessor

processor = FaceProcessor()
result = processor.process_image("test_image.jpg")

if result:
    print(f"✅ Phát hiện {result['total_faces']} khuôn mặt")
    for i, face in enumerate(result['faces']):
        print(f"Face {i+1}: confidence = {face['confidence']:.3f}")
else:
    print("❌ Không phát hiện được khuôn mặt")
```

## ⚙️ Bước 7: Điều chỉnh cấu hình

Chỉnh sửa file `config.py`:

```python
# Cấu hình database
DATABASE_CONFIG = {
    'host': 'localhost',        # Thay đổi nếu DB ở server khác
    'port': 3306,
    'user': 'root',            # Username MySQL
    'password': 'your_password', # Password MySQL
    'database': 'smartparking'   # Tên database
}

# Cấu hình face recognition
FACE_SIMILARITY_THRESHOLD = 0.6    # Thay đổi ngưỡng (0.5-0.8)

# Cấu hình ảnh
TEST_IMAGE_PATHS = {
    'test_image_1': 'path/to/your/test1.jpg',
    'test_image_2': 'path/to/your/test2.jpg'
}
```

## 🚨 Troubleshooting phổ biến

### Lỗi 1: Không kết nối được database
```bash
❌ Error 2003: Can't connect to MySQL server
```
**Giải pháp:**
- Kiểm tra MySQL đã chạy chưa
- Kiểm tra username/password trong config.py
- Kiểm tra tên database có tồn tại không

### Lỗi 2: Không phát hiện được khuôn mặt
```bash
❌ Không tìm thấy khuôn mặt trong ảnh
```
**Giải pháp:**
- Sử dụng ảnh có độ phân giải cao hơn
- Đảm bảo khuôn mặt rõ nét, không bị che
- Thử ảnh có ánh sáng tốt hơn

### Lỗi 3: Accuracy thấp
```bash
⚠️ Similarity thấp, nhận diện sai
```
**Giải pháp:**
- Giảm threshold từ 0.6 xuống 0.5
- Đăng ký với nhiều ảnh của cùng một người
- Sử dụng ảnh chất lượng cao khi đăng ký

## 🎯 Tips sử dụng hiệu quả

1. **📸 Chất lượng ảnh**: Ảnh rõ nét, khuôn mặt chiếm ít nhất 100x100 pixels
2. **🎚️ Threshold**: Bắt đầu với 0.6, điều chỉnh theo nhu cầu
3. **💾 Database**: Backup database thường xuyên
4. **⚡ Performance**: Resize ảnh xuống kích thước hợp lý để xử lý nhanh hơn
5. **🔄 Update**: Đăng ký lại với ảnh mới khi appearance thay đổi nhiều

---
**🎉 Chúc bạn sử dụng hệ thống hiệu quả!**