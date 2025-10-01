# 🚀 FACE RECOGNITION FASTAPI SERVER - COMPLETE SETUP

Hệ thống nhận diện khuôn mặt sử dụng **FastAPI + YOLOv8 + InsightFace** với khả năng tích hợp Spring Boot backend.

## 📁 Files Setup quan trọng

| File | Mô tả | Cách sử dụng |
|------|-------|--------------|
| `setup_face_recognition.py` | **Script setup tự động chính** | `python setup_face_recognition.py` |
| `system_check.py` | Kiểm tra hệ thống trước cài đặt | `python system_check.py` |
| `INSTALLATION_GUIDE.md` | Hướng dẫn chi tiết từng bước | Đọc khi gặp vấn đề |
| `face_fastapi_server.py` | Server chính | `python face_fastapi_server.py` |

## ⚡ Quick Start (30 giây)

### 1. Kiểm tra hệ thống:
```bash
python system_check.py
```

### 2. Cài đặt tự động:
```bash
python setup_face_recognition.py
```

### 3. Khởi động server:
```bash
python face_fastapi_server.py
```

### 4. Test API:
- 🏥 Health check: http://localhost:8000/api/v1/simple-face/health
- 📚 API docs: http://localhost:8000/docs

## 🎯 API Endpoints (Spring Boot Compatible)

| Method | Endpoint | Chức năng |
|--------|----------|-----------|
| GET | `/api/v1/simple-face/health` | Health check |
| GET | `/api/v1/simple-face/test` | Test endpoint |
| POST | `/api/v1/simple-face/register` | Đăng ký khuôn mặt |
| POST | `/api/v1/simple-face/recognize` | Nhận diện khuôn mặt |
| POST | `/api/v1/simple-face/compare` | So sánh 2 khuôn mặt |
| GET | `/api/v1/simple-face/list` | Danh sách khuôn mặt |
| DELETE | `/api/v1/simple-face/delete/{id}` | Xóa khuôn mặt |

## 🔧 Cấu hình hệ thống

### Yêu cầu tối thiểu:
- **Python 3.8+**
- **MySQL 8.0+**
- **RAM 8GB+**
- **Ổ cứng 10GB+**

### Optional (tăng performance):
- **NVIDIA GPU** với CUDA 11.8+
- **SSD storage**
- **16GB+ RAM**

## 📊 Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACE RECOGNITION SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│  🌐 FastAPI Server (face_fastapi_server.py)                    │
│  ├── Spring Boot Compatible API endpoints                       │
│  ├── Async request handling                                     │
│  ├── Base64 image processing                                    │
│  └── Error handling & logging                                   │
├─────────────────────────────────────────────────────────────────┤
│  🧠 Face Recognition System (face_recognition_system.py)       │
│  ├── Register faces from base64                                 │
│  ├── Recognize faces with threshold                             │
│  ├── Compare two faces                                          │
│  └── Manage face embeddings                                     │
├─────────────────────────────────────────────────────────────────┤
│  🔍 Face Processor (face_processor.py)                         │
│  ├── YOLOv8 Face Detection                                      │
│  ├── InsightFace Feature Extraction                             │
│  ├── Cosine similarity calculation                              │
│  └── GPU/CPU optimization                                       │
├─────────────────────────────────────────────────────────────────┤
│  🗄️ Database Manager (database_manager.py)                     │
│  ├── MySQL connection handling                                  │
│  ├── Face embedding storage (JSON)                              │
│  ├── CRUD operations                                            │
│  └── Transaction management                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Tính năng chính

### ✅ Face Registration
- Đăng ký khuôn mặt từ base64 image
- Lưu trữ embedding vector trong MySQL
- Support mô tả (description) cho mỗi khuôn mặt
- Validation ảnh input

### ✅ Face Recognition  
- Nhận diện khuôn mặt real-time
- Configurable similarity threshold
- Trả về thông tin chi tiết (name, face_id, similarity, confidence)
- Xử lý multiple faces trong 1 ảnh

### ✅ Face Comparison
- So sánh 2 khuôn mặt trực tiếp
- Similarity score calculation
- Boolean match result
- Processing time tracking

### ✅ Face Management
- List tất cả khuôn mặt đã đăng ký
- Delete khuôn mặt theo ID
- Search và filter
- Backup/restore capability

## 🔧 Customization

### Thay đổi similarity threshold:
```python
# Trong face_processor.py
FACE_SIMILARITY_THRESHOLD = 0.6  # Default
```

### Database configuration:
```python
# Trong database_manager.py
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'face_recognition_db'
}
```

### Server configuration:
```python
# Trong face_fastapi_server.py
if __name__ == "__main__":
    uvicorn.run(
        "face_fastapi_server:app",
        host="0.0.0.0",      # Bind to all interfaces
        port=8000,           # Port number
        reload=True,         # Auto-reload on code changes
        log_level="info"     # Logging level
    )
```

## 🐳 Docker Deployment

### Sử dụng Docker Compose:
```bash
# Build và run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f face-recognition-api

# Stop
docker-compose down
```

### Custom Docker build:
```bash
# Build image
docker build -t face-recognition-api .

# Run container
docker run -p 8000:8000 face-recognition-api
```

## 📈 Performance Optimization

### GPU Acceleration:
```bash
# Install CUDA packages
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install onnxruntime-gpu

# Set environment
export CUDA_VISIBLE_DEVICES=0
```

### Memory Optimization:
```python
# Reduce batch size for low memory
BATCH_SIZE = 1

# Use smaller models
MODEL_NAME = "yolov8n-face.pt"  # Nano version
```

### Database Indexing:
```sql
-- Add indexes for better performance
CREATE INDEX idx_name ON faces(name);
CREATE INDEX idx_created_at ON faces(created_at);
```

## 🚨 Troubleshooting

### Lỗi thường gặp:

#### 1. "ModuleNotFoundError: No module named 'insightface'"
```bash
pip install insightface==0.7.3
# Hoặc
pip install insightface --no-binary insightface
```

#### 2. "CUDA out of memory"
```python
# Giảm batch size trong config
BATCH_SIZE = 1
# Hoặc sử dụng CPU
USE_GPU = False
```

#### 3. "MySQL connection refused"
```bash
# Start MySQL service
# Windows:
net start mysql
# Linux:
sudo systemctl start mysql
```

#### 4. "Port 8000 already in use"
```bash
# Find và kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Debug logging:
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Examples

### Register Face:
```python
import requests
import base64

# Read image
with open('person.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Register
response = requests.post('http://localhost:8000/api/v1/simple-face/register', json={
    'name': 'John Doe',
    'image': f'data:image/jpeg;base64,{image_data}',
    'description': 'Employee ID: 12345'
})

print(response.json())
```

### Recognize Face:
```python
# Recognize
response = requests.post('http://localhost:8000/api/v1/simple-face/recognize', json={
    'image': f'data:image/jpeg;base64,{image_data}',
    'threshold': 0.6
})

result = response.json()
if result['success'] and result['name']:
    print(f"Recognized: {result['name']} (similarity: {result['similarity']:.3f})")
else:
    print("No match found")
```

### Compare Faces:
```python
# Compare two images
response = requests.post('http://localhost:8000/api/v1/simple-face/compare', json={
    'image1': f'data:image/jpeg;base64,{image1_data}',
    'image2': f'data:image/jpeg;base64,{image2_data}',
    'threshold': 0.6
})

result = response.json()
print(f"Similarity: {result['similarity']:.3f}, Match: {result['match']}")
```

## 🔐 Security Considerations

### Production deployment:
- Add API authentication (JWT tokens)
- Implement rate limiting
- Use HTTPS/SSL certificates
- Restrict CORS origins
- Add input validation
- Use environment variables for secrets

### Example security middleware:
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "*.example.com"])
app.add_middleware(HTTPSRedirectMiddleware)
```

## 📞 Support & Contributing

### Issues:
- Check logs in `logs/` directory
- Run `python system_check.py` để kiểm tra hệ thống
- Xem INSTALLATION_GUIDE.md để troubleshooting

### Contributing:
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

---

## 🎉 Kết luận

Hệ thống Face Recognition FastAPI Server cung cấp:

✅ **High Performance**: FastAPI async processing  
✅ **Accurate Recognition**: YOLOv8 + InsightFace  
✅ **Spring Boot Compatible**: Tương thích hoàn toàn  
✅ **Easy Deployment**: Docker support  
✅ **Scalable**: Database-backed storage  
✅ **Production Ready**: Comprehensive error handling  

**Bắt đầu ngay:** `python setup_face_recognition.py`

---

*Happy coding! 🚀*