# 🚀 FACE RECOGNITION API SERVER

API Server cho hệ thống nhận diện khuôn mặt, tích hợp với Java Spring Boot backend.

## 📋 API Endpoints

### 1. 🏥 Health Check
**GET** `/api/health`

Kiểm tra trạng thái hệ thống.

**Response:**
```json
{
    "status": "OK",
    "message": "Face Recognition API đang hoạt động",
    "timestamp": "2025-09-29T10:30:00.000Z",
    "total_registered_faces": 15,
    "version": "1.0.0"
}
```

### 2. 📝 Đăng ký khuôn mặt
**POST** `/api/face/register`

**Request Body (JSON):**
```json
{
    "name": "Nguyễn Văn A",
    "image": "base64_string_của_ảnh",
    "description": "Nhân viên IT (optional)"
}
```

**Hoặc Form-data:**
- `name`: Tên người
- `image`: File ảnh
- `description`: Mô tả (optional)

**Response thành công:**
```json
{
    "success": true,
    "message": "Đăng ký khuôn mặt thành công",
    "data": {
        "face_id": 123,
        "person_name": "Nguyễn Văn A",
        "confidence": 0.95,
        "embedding_dimension": 512,
        "description": "Nhân viên IT"
    }
}
```

### 3. 🔍 Nhận diện khuôn mặt
**POST** `/api/face/recognize`

**Request Body (JSON):**
```json
{
    "image": "base64_string_của_ảnh",
    "threshold": 0.6
}
```

**Response thành công:**
```json
{
    "success": true,
    "message": "Nhận diện thành công 2 khuôn mặt",
    "data": {
        "total_faces": 2,
        "threshold_used": 0.6,
        "faces": [
            {
                "face_index": 1,
                "bounding_box": {
                    "x1": 100,
                    "y1": 50,
                    "x2": 200,
                    "y2": 150
                },
                "detection_confidence": 0.92,
                "match_found": true,
                "person_name": "Nguyễn Văn A",
                "match_similarity": 0.85,
                "face_id": 123,
                "best_similarity": 0.85
            },
            {
                "face_index": 2,
                "bounding_box": {
                    "x1": 300,
                    "y1": 60,
                    "x2": 400,
                    "y2": 160
                },
                "detection_confidence": 0.88,
                "match_found": false,
                "best_similarity": 0.45
            }
        ]
    }
}
```

### 4. ⚖️ So sánh hai ảnh
**POST** `/api/face/compare`

**Request Body (JSON):**
```json
{
    "image1": "base64_string_ảnh_1",
    "image2": "base64_string_ảnh_2",
    "threshold": 0.6
}
```

**Response thành công:**
```json
{
    "success": true,
    "message": "So sánh thành công",
    "data": {
        "similarity": 0.89,
        "is_same_person": true,
        "threshold": 0.6,
        "confidence": 0.29,
        "image1_info": {
            "faces_count": 1,
            "detection_confidence": 0.95
        },
        "image2_info": {
            "faces_count": 1,
            "detection_confidence": 0.92
        }
    }
}
```

### 5. 📊 Danh sách khuôn mặt đã đăng ký
**GET** `/api/face/list`

**Response:**
```json
{
    "success": true,
    "message": "Tìm thấy 15 khuôn mặt đã đăng ký",
    "data": {
        "total_faces": 15,
        "faces": [
            {
                "face_id": 123,
                "name": "Nguyễn Văn A",
                "embedding_dimension": 512
            },
            {
                "face_id": 124,
                "name": "Trần Thị B",
                "embedding_dimension": 512
            }
        ]
    }
}
```

### 6. 🗑️ Xóa khuôn mặt
**DELETE** `/api/face/delete/{face_id}`

**Response:**
```json
{
    "success": true,
    "message": "Đã xóa khuôn mặt ID 123"
}
```

## 🚀 Cách chạy API Server

### 1. Cài đặt dependencies
```bash
pip install -r api_requirements.txt
```

### 2. Chạy server
```bash
python face_api_server.py
```

Server sẽ chạy tại: `http://localhost:5000`

## 📝 Tích hợp với Java Spring Boot

### 1. Dependency cho Spring Boot
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

### 2. Service class Java
```java
@Service
public class FaceRecognitionService {
    
    private final WebClient webClient;
    private final String API_BASE_URL = "http://localhost:5000/api";
    
    public FaceRecognitionService() {
        this.webClient = WebClient.builder()
            .baseUrl(API_BASE_URL)
            .build();
    }
    
    // Đăng ký khuôn mặt
    public Mono<FaceRegisterResponse> registerFace(String name, String base64Image) {
        FaceRegisterRequest request = new FaceRegisterRequest(name, base64Image);
        
        return webClient.post()
            .uri("/face/register")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(FaceRegisterResponse.class);
    }
    
    // Nhận diện khuôn mặt
    public Mono<FaceRecognizeResponse> recognizeFace(String base64Image, Double threshold) {
        FaceRecognizeRequest request = new FaceRecognizeRequest(base64Image, threshold);
        
        return webClient.post()
            .uri("/face/recognize")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(FaceRecognizeResponse.class);
    }
    
    // So sánh hai ảnh
    public Mono<FaceCompareResponse> compareFaces(String base64Image1, String base64Image2) {
        FaceCompareRequest request = new FaceCompareRequest(base64Image1, base64Image2);
        
        return webClient.post()
            .uri("/face/compare")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(FaceCompareResponse.class);
    }
}
```

### 3. Controller Java
```java
@RestController
@RequestMapping("/api/v1/face")
public class FaceRecognitionController {
    
    @Autowired
    private FaceRecognitionService faceService;
    
    @PostMapping("/register")
    public Mono<ResponseEntity<FaceRegisterResponse>> registerFace(
            @RequestBody FaceRegisterRequest request) {
        
        return faceService.registerFace(request.getName(), request.getImage())
            .map(response -> ResponseEntity.ok(response))
            .onErrorReturn(ResponseEntity.badRequest().build());
    }
    
    @PostMapping("/recognize")
    public Mono<ResponseEntity<FaceRecognizeResponse>> recognizeFace(
            @RequestBody FaceRecognizeRequest request) {
        
        return faceService.recognizeFace(request.getImage(), request.getThreshold())
            .map(response -> ResponseEntity.ok(response))
            .onErrorReturn(ResponseEntity.badRequest().build());
    }
    
    @PostMapping("/compare")
    public Mono<ResponseEntity<FaceCompareResponse>> compareFaces(
            @RequestBody FaceCompareRequest request) {
        
        return faceService.compareFaces(request.getImage1(), request.getImage2())
            .map(response -> ResponseEntity.ok(response))
            .onErrorReturn(ResponseEntity.badRequest().build());
    }
}
```

## 🔧 Cấu hình Production

### 1. Sử dụng Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 face_api_server:app
```

### 2. Docker (optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "face_api_server:app"]
```

## ⚠️ Lưu ý

1. **CORS**: API đã được cấu hình CORS để Spring Boot có thể gọi
2. **File upload**: Hỗ trợ cả base64 và multipart/form-data
3. **Error handling**: Trả về JSON response nhất quán
4. **Logging**: Ghi log chi tiết cho debugging
5. **Cleanup**: Tự động xóa file tạm sau khi xử lý

## 🧪 Test API

Sử dụng Postman hoặc curl để test:

```bash
# Health check
curl http://localhost:5000/api/health

# Test đăng ký (với file)
curl -X POST \
  -F "name=Test User" \
  -F "image=@/path/to/image.jpg" \
  http://localhost:5000/api/face/register
```