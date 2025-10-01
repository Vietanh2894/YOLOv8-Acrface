# Face Recognition Java Spring Boot Integration

## Tổng Quan

Đây là tích hợp hoàn chỉnh của hệ thống Face Recognition vào Java Spring Boot sử dụng Python API backend.

## Kiến Trúc

```
Python API (Flask)  <-->  Java Spring Boot  <-->  Client Application
     Port 5000              Port 8080              Frontend/Mobile
```

## Cài Đặt và Chạy

### 1. Khởi động Python API Server

```bash
cd c:\Users\ADMIN\Documents\NGHIENCUUKHOAHOC\insightface
python face_api_server.py
```

API sẽ chạy trên: `http://localhost:5000`

### 2. Cấu hình Java Spring Boot

#### Maven Dependencies (pom.xml)

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
</dependencies>
```

#### Cấu hình Application Properties

```properties
face.api.base-url=http://localhost:5000/api
face.api.timeout.connection=30
face.api.timeout.response=60
server.port=8080
spring.servlet.multipart.max-file-size=10MB
```

### 3. Cấu trúc Package

```
com.example.facerecognition/
├── FaceRecognitionApplication.java     # Main class
├── config/
│   └── FaceRecognitionConfig.java      # WebClient config
├── controller/
│   └── FaceRecognitionController.java  # REST endpoints
├── service/
│   └── FaceRecognitionService.java     # Business logic
└── dto/                                # Data transfer objects
```

### 4. Chạy Spring Boot Application

```bash
mvn spring-boot:run
```

hoặc

```bash
java -jar target/face-recognition-api-1.0.0.jar
```

## API Endpoints

### Java Spring Boot Endpoints (Port 8080)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/face/health` | Kiểm tra trạng thái |
| POST | `/api/v1/face/register` | Đăng ký khuôn mặt (base64) |
| POST | `/api/v1/face/register-file` | Đăng ký khuôn mặt (file) |
| POST | `/api/v1/face/recognize` | Nhận diện (base64) |
| POST | `/api/v1/face/recognize-file` | Nhận diện (file) |
| POST | `/api/v1/face/compare` | So sánh (base64) |
| POST | `/api/v1/face/compare-files` | So sánh (file) |
| GET | `/api/v1/face/list` | Danh sách đã đăng ký |
| DELETE | `/api/v1/face/delete/{id}` | Xóa khuôn mặt |

### Python API Endpoints (Port 5000)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/health` | Health check |
| POST | `/api/face/register` | Đăng ký khuôn mặt |
| POST | `/api/face/recognize` | Nhận diện khuôn mặt |
| POST | `/api/face/compare` | So sánh hai khuôn mặt |
| GET | `/api/face/list` | Danh sách khuôn mặt |
| DELETE | `/api/face/delete/{id}` | Xóa khuôn mặt |

## Sử Dụng API

### 1. Đăng ký khuôn mặt với file upload

```bash
curl -X POST http://localhost:8080/api/v1/face/register-file \
  -F "name=John Doe" \
  -F "image=@path/to/image.jpg" \
  -F "description=Employee"
```

### 2. Nhận diện khuôn mặt với base64

```bash
curl -X POST http://localhost:8080/api/v1/face/recognize \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64_encoded_image",
    "threshold": 0.6
  }'
```

### 3. So sánh hai khuôn mặt

```bash
curl -X POST http://localhost:8080/api/v1/face/compare-files \
  -F "image1=@image1.jpg" \
  -F "image2=@image2.jpg" \
  -F "threshold=0.6"
```

### 4. Lấy danh sách khuôn mặt đã đăng ký

```bash
curl -X GET http://localhost:8080/api/v1/face/list
```

## Tích Hợp Vào Project

### 1. Copy các file Java vào project

```
src/main/java/com/yourpackage/
├── config/FaceRecognitionConfig.java
├── controller/FaceRecognitionController.java
└── service/FaceRecognitionService.java
```

### 2. Thêm dependencies vào pom.xml

### 3. Cấu hình application.properties

### 4. Inject service vào controller khác

```java
@RestController
public class YourController {
    
    @Autowired
    private FaceRecognitionService faceService;
    
    @PostMapping("/your-endpoint")
    public Mono<ResponseEntity<?>> yourMethod() {
        return faceService.recognizeFace(image, 0.6)
            .map(response -> ResponseEntity.ok(response));
    }
}
```

## Features

### ✅ Đã Hoàn Thành

- **Base64 & File Upload**: Hỗ trợ cả base64 string và multipart file upload
- **Reactive Programming**: Sử dụng WebFlux với Mono/Flux
- **Error Handling**: Xử lý lỗi toàn diện
- **CORS Support**: Cấu hình CORS cho frontend integration
- **Timeout Configuration**: Cấu hình timeout cho API calls
- **Validation**: Validate input parameters
- **Documentation**: API documentation và examples

### 📋 Request/Response Models

```java
// Register Request
{
  "name": "John Doe",
  "image": "base64_encoded_image",
  "description": "Employee"
}

// Recognize Response
{
  "success": true,
  "message": "Face recognized",
  "name": "John Doe",
  "face_id": 1,
  "similarity": 0.85
}

// Compare Response
{
  "success": true,
  "message": "Faces compared successfully",
  "similarity": 0.92,
  "match": true
}
```

## Testing

### Unit Tests

```bash
mvn test
```

### Integration Tests với Python API

1. Đảm bảo Python API đang chạy
2. Chạy Spring Boot tests
3. Test thông qua Postman hoặc curl

## Troubleshooting

### 1. Connection Refused

- Kiểm tra Python API có đang chạy không
- Verify port 5000 không bị block

### 2. Timeout Issues

- Tăng timeout trong application.properties
- Kiểm tra kích thước ảnh (< 10MB)

### 3. CORS Issues

- Cấu hình CORS trong Spring Boot
- Check `@CrossOrigin` annotation

## Production Deployment

### Python API
```bash
gunicorn -w 4 -b 0.0.0.0:5000 face_api_server:app
```

### Spring Boot
```bash
java -jar -Dspring.profiles.active=prod face-recognition-api.jar
```

## Monitoring và Logging

- Health check endpoints
- Detailed error logging
- Performance monitoring với Micrometer
- API usage metrics

---

**Lưu ý**: Đảm bảo cả Python API và Java Spring Boot đều đang chạy để system hoạt động đầy đủ.