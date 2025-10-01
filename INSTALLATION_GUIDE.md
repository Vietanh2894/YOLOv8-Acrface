# HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY FACE RECOGNITION FASTAPI SERVER

## 📋 Tổng quan

File này hướng dẫn chi tiết cách cài đặt và chạy Face Recognition FastAPI Server từ đầu đến cuối.

## 🎯 Yêu cầu hệ thống

### Phần mềm bắt buộc:
- **Python 3.8+** (khuyến nghị Python 3.9 hoặc 3.10)
- **MySQL 8.0+** hoặc MariaDB 10.5+
- **Git** (để clone repository)

### Phần cứng khuyến nghị:
- **RAM**: Tối thiểu 8GB, khuyến nghị 16GB+
- **CPU**: Intel i5/AMD Ryzen 5 trở lên
- **GPU**: NVIDIA GPU với CUDA 11.8+ (tùy chọn, để tăng tốc độ)
- **Ổ cứng**: 10GB dung lượng trống

## 🚀 Cách 1: Tự động cài đặt (Khuyến nghị)

### Bước 1: Chạy script setup
```bash
python setup_face_recognition.py
```

Script sẽ tự động:
- ✅ Kiểm tra Python version
- ✅ Cài đặt tất cả packages cần thiết
- ✅ Kiểm tra GPU support
- ✅ Tạo thư mục cần thiết
- ✅ Download AI models
- ✅ Thiết lập database
- ✅ Tạo file cấu hình
- ✅ Tạo startup scripts
- ✅ Test toàn bộ hệ thống

### Bước 2: Khởi động server
Sau khi setup hoàn tất, chọn `y` để khởi động server ngay lập tức.

## 🔧 Cách 2: Cài đặt thủ công

### Bước 1: Cài đặt Python packages

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install FastAPI và web framework
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.5.0
pip install python-multipart==0.0.6

# Install AI/ML packages
pip install opencv-python==4.8.1.78
pip install pillow==10.1.0
pip install numpy==1.24.3
pip install insightface==0.7.3
pip install ultralytics==8.0.206
pip install scikit-learn==1.3.2
pip install matplotlib==3.8.2

# Install database
pip install pymysql==1.1.0
pip install cryptography==41.0.7

# Install ONNX Runtime
pip install onnxruntime==1.16.3
# Hoặc GPU version (nếu có NVIDIA GPU)
pip install onnxruntime-gpu==1.16.3

# Install utilities
pip install requests==2.31.0
```

### Bước 2: Thiết lập thư mục

```bash
mkdir models
mkdir logs
mkdir temp
mkdir data
mkdir uploads
```

### Bước 3: Download AI Models

#### YOLOv8 Face Detection Model:
```bash
# Download YOLOv8 Face model
curl -L "https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt" -o "models/yolov8n-face.pt"
```

#### InsightFace Model:
```bash
# Download và giải nén InsightFace buffalo_l model
curl -L "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip" -o "temp/buffalo_l.zip"
unzip temp/buffalo_l.zip -d models/
rm temp/buffalo_l.zip
```

### Bước 4: Thiết lập MySQL Database

#### Tạo database:
```sql
CREATE DATABASE face_recognition_db;
USE face_recognition_db;

CREATE TABLE faces (
    face_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    embedding JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### Cấu hình database trong code:
Cập nhật thông tin database trong `database_manager.py`:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'face_recognition_db'
}
```

### Bước 5: Khởi động server

```bash
python face_fastapi_server.py
```

## 🐳 Cách 3: Sử dụng Docker

### Prerequisites:
- Docker Desktop
- Docker Compose

### Chạy với Docker:

```bash
# Build và chạy
docker-compose up --build

# Chạy ở background
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

## 📊 Kiểm tra cài đặt

### 1. Test server health:
```bash
curl http://localhost:8000/api/v1/simple-face/health
```

### 2. Xem API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Test endpoints:

#### Register face:
```bash
curl -X POST "http://localhost:8000/api/v1/simple-face/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "image": "data:image/jpeg;base64,/9j/4AAQ...",
    "description": "Test registration"
  }'
```

#### Recognize face:
```bash
curl -X POST "http://localhost:8000/api/v1/simple-face/recognize" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQ...",
    "threshold": 0.6
  }'
```

## 🔧 Cấu hình nâng cao

### GPU Acceleration (NVIDIA):

```bash
# Install CUDA packages
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install onnxruntime-gpu

# Set environment variables
export CUDA_VISIBLE_DEVICES=0
export OMP_NUM_THREADS=4
```

### Performance Tuning:

#### Trong `config.py`:
```python
FACE_RECOGNITION_CONFIG = {
    'similarity_threshold': 0.6,      # Ngưỡng nhận diện
    'max_faces_per_image': 5,         # Số face tối đa mỗi ảnh
    'yolo_confidence': 0.5,           # Confidence threshold cho YOLO
    'yolo_iou': 0.45,                 # IoU threshold cho NMS
    'insightface_ctx_id': 0,          # GPU context ID (-1 cho CPU)
    'enable_gpu': True                # Bật GPU acceleration
}
```

### Database Optimization:

```sql
-- Tối ưu MySQL cho face embeddings
SET innodb_buffer_pool_size = 2G;
SET max_connections = 200;
CREATE INDEX idx_embedding_hash ON faces(MD5(embedding));
```

### Production Deployment:

#### Nginx Configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;
    }
}
```

#### SSL/HTTPS Setup:
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

## 🚨 Troubleshooting

### Lỗi thường gặp:

#### 1. Import Error - InsightFace:
```bash
# Cài đặt lại InsightFace
pip uninstall insightface
pip install insightface==0.7.3

# Hoặc build từ source
pip install insightface --no-binary insightface
```

#### 2. CUDA/GPU Issues:
```bash
# Kiểm tra CUDA
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall CUDA packages
pip uninstall torch torchvision onnxruntime-gpu
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install onnxruntime-gpu
```

#### 3. MySQL Connection Error:
```python
# Test connection
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='face_recognition_db'
)
print("Connection successful!")
```

#### 4. Model Download Issues:
```bash
# Manual download
wget https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt -O models/yolov8n-face.pt
wget https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip -O temp/buffalo_l.zip
```

#### 5. Memory Issues:
```python
# Trong face_processor.py, giảm batch size
BATCH_SIZE = 1  # Thay vì 4 hoặc 8

# Hoặc tăng swap memory
sudo swapon --show
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📈 Monitoring & Logging

### Log Files:
- Server logs: `logs/server.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

### Health Monitoring:
```bash
# Script monitor.sh
#!/bin/bash
while true; do
    curl -s http://localhost:8000/api/v1/simple-face/health | jq
    sleep 60
done
```

### Performance Metrics:
```python
# Thêm vào server
import psutil
import GPUtil

@app.get("/api/v1/simple-face/metrics")
async def get_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "gpu_usage": GPUtil.getGPUs()[0].load * 100 if GPUtil.getGPUs() else 0
    }
```

## 🎯 Next Steps

Sau khi cài đặt thành công:

1. **Test với ảnh thật**: Upload ảnh của bạn để test
2. **Tích hợp với ứng dụng**: Sử dụng API endpoints trong ứng dụng của bạn
3. **Tối ưu performance**: Điều chỉnh threshold và parameters
4. **Backup database**: Thiết lập backup định kỳ cho MySQL
5. **Security**: Thêm authentication và rate limiting
6. **Monitoring**: Thiết lập monitoring và alerting

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong thư mục `logs/`
2. Chạy `python setup_face_recognition.py` để test lại
3. Xem phần Troubleshooting ở trên
4. Check GitHub issues và documentation

---

**Chúc bạn cài đặt thành công! 🎉**