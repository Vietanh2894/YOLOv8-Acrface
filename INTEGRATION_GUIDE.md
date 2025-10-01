# Hướng Dẫn Tích Hợp Face Recognition vào Java Spring Boot Backend

## 📋 Bước 1: Copy Files vào Project

### Cấu trúc thư mục trong Spring Boot project:
```
src/main/java/com/yourcompany/yourproject/
├── config/
│   └── FaceRecognitionConfig.java     ✅ Copy file này
├── controller/
│   └── FaceRecognitionController.java ✅ Copy file này  
├── service/
│   └── FaceRecognitionService.java    ✅ Copy file này
└── dto/                               ✅ Tạo thư mục mới
    └── face/                          ✅ DTOs được define trong Service
```

## 📦 Bước 2: Thêm Dependencies vào pom.xml

```xml
<!-- Thêm vào <dependencies> section -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

## ⚙️ Bước 3: Cấu hình application.properties

```properties
# Face Recognition API Configuration
face.api.base-url=http://localhost:5000/api
face.api.timeout.connection=30
face.api.timeout.response=60

# Multipart file upload size
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

## 🔧 Bước 4: Sử Dụng trong Controller hiện có

### Ví dụ tích hợp vào Employee Controller:

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {
    
    @Autowired
    private EmployeeService employeeService;
    
    @Autowired  // ✅ Inject Face Recognition Service
    private FaceRecognitionService faceService;
    
    // ✅ Endpoint đăng ký khuôn mặt cho nhân viên
    @PostMapping("/{employeeId}/register-face")
    public Mono<ResponseEntity<?>> registerEmployeeFace(
            @PathVariable Long employeeId,
            @RequestParam("photo") MultipartFile photo) {
        
        Employee employee = employeeService.findById(employeeId);
        String base64Image = convertToBase64(photo);
        
        return faceService.registerFace(
                employee.getName(), 
                base64Image, 
                "Employee ID: " + employeeId
            )
            .map(response -> {
                if (response.getSuccess()) {
                    // Lưu face_id vào employee record
                    employee.setFaceId(response.getFaceId());
                    employeeService.save(employee);
                    
                    return ResponseEntity.ok("Face registered successfully");
                } else {
                    return ResponseEntity.badRequest()
                        .body("Failed: " + response.getMessage());
                }
            });
    }
    
    // ✅ Endpoint xác thực nhân viên bằng khuôn mặt
    @PostMapping("/verify-face")
    public Mono<ResponseEntity<?>> verifyEmployee(
            @RequestParam("photo") MultipartFile photo) {
        
        String base64Image = convertToBase64(photo);
        
        return faceService.recognizeFace(base64Image, 0.7)
            .map(response -> {
                if (response.getSuccess() && response.getSimilarity() > 0.8) {
                    // Tìm employee theo face_id
                    Employee employee = employeeService.findByFaceId(response.getFaceId());
                    
                    return ResponseEntity.ok(Map.of(
                        "verified", true,
                        "employee", employee,
                        "similarity", response.getSimilarity()
                    ));
                } else {
                    return ResponseEntity.status(401)
                        .body(Map.of("verified", false, "message", "Face not recognized"));
                }
            });
    }
    
    // Helper method
    private String convertToBase64(MultipartFile file) {
        try {
            return Base64.getEncoder().encodeToString(file.getBytes());
        } catch (IOException e) {
            throw new RuntimeException("Failed to convert image", e);
        }
    }
}
```

### Ví dụ tích hợp vào Security/Authentication:

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    
    @Autowired
    private FaceRecognitionService faceService;
    
    @Autowired
    private JwtTokenProvider tokenProvider;
    
    @PostMapping("/face-login")
    public Mono<ResponseEntity<?>> faceLogin(
            @RequestParam("photo") MultipartFile photo) {
        
        String base64Image = convertToBase64(photo);
        
        return faceService.recognizeFace(base64Image, 0.75)
            .map(response -> {
                if (response.getSuccess() && response.getSimilarity() > 0.8) {
                    // Tạo JWT token
                    String token = tokenProvider.createToken(response.getName());
                    
                    return ResponseEntity.ok(Map.of(
                        "token", token,
                        "user", response.getName(),
                        "similarity", response.getSimilarity()
                    ));
                } else {
                    return ResponseEntity.status(401)
                        .body(Map.of("error", "Authentication failed"));
                }
            });
    }
}
```

## 🏃‍♂️ Bước 5: Chạy Hệ Thống

### Terminal 1: Python API
```bash
cd C:\Users\ADMIN\Documents\NGHIENCUUKHOAHOC\insightface
python face_api_server.py
```

### Terminal 2: Java Spring Boot
```bash
cd /path/to/your/springboot/project
mvn spring-boot:run
```

## 🧪 Bước 6: Test API

```bash
# Test face registration
curl -X POST http://localhost:8080/api/employees/1/register-face \
  -F "photo=@employee_photo.jpg"

# Test face verification  
curl -X POST http://localhost:8080/api/employees/verify-face \
  -F "photo=@test_photo.jpg"

# Test face login
curl -X POST http://localhost:8080/api/auth/face-login \
  -F "photo=@login_photo.jpg"
```

## 🎯 Lợi Ích của Cách Tích Hợp Này:

✅ **Đơn giản**: Chỉ cần copy 3 files và thêm 1 dependency
✅ **Linh hoạt**: Sử dụng face recognition trong bất kỳ controller nào
✅ **Reactive**: Hỗ trợ lập trình bất đồng bộ với Mono/Flux
✅ **Scalable**: Dễ dàng mở rộng thêm features
✅ **Maintainable**: Code được tổ chức rõ ràng

## 🔧 Troubleshooting:

1. **Connection refused**: Đảm bảo Python API đang chạy trên port 5000
2. **Image too large**: Tăng `spring.servlet.multipart.max-file-size`
3. **Timeout**: Tăng `face.api.timeout.response` trong config
4. **CORS issues**: Thêm `@CrossOrigin` annotation nếu cần

## 📝 Next Steps:

1. Thêm Face ID vào Employee entity
2. Implement face verification trong authentication flow
3. Add logging và monitoring
4. Deploy to production with proper security