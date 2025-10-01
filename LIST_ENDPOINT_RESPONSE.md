# 📋 API ENDPOINT: GET /api/v1/simple-face/list

## 🎯 **Response Format**

### ✅ **Success Response:**

```json
{
    "success": true,
    "message": "Retrieved 15 faces",
    "faces": [
        {
            "face_id": 123,
            "name": "Nguyễn Văn A",
            "description": "Nhân viên IT phòng Dev",
            "created_at": "2025-09-30 10:30:45",
            "updated_at": "2025-09-30 10:30:45"
        },
        {
            "face_id": 124,
            "name": "Trần Thị B", 
            "description": null,
            "created_at": "2025-09-30 09:15:22",
            "updated_at": "2025-09-30 09:15:22"
        },
        {
            "face_id": 125,
            "name": "Lê Văn C",
            "description": "Manager phòng Marketing",
            "created_at": "2025-09-29 14:20:33",
            "updated_at": "2025-09-29 14:20:33"
        }
    ],
    "count": 3
}
```

### ❌ **Error Response:**

```json
{
    "success": false,
    "message": "Failed to retrieve faces: Database connection error",
    "faces": [],
    "count": 0
}
```

## 📊 **Response Schema**

### **Root Object:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | `boolean` | Trạng thái thành công/thất bại |
| `message` | `string` | Thông báo kết quả |
| `faces` | `array` | Danh sách khuôn mặt đã đăng ký |
| `count` | `integer` | Tổng số khuôn mặt |

### **FaceInfo Object:**
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `face_id` | `integer` | ID duy nhất của khuôn mặt | `123` |
| `name` | `string` | Tên người được đăng ký | `"Nguyễn Văn A"` |
| `description` | `string/null` | Mô tả thêm (có thể null) | `"Nhân viên IT"` |
| `created_at` | `string` | Thời gian tạo (ISO format) | `"2025-09-30 10:30:45"` |
| `updated_at` | `string` | Thời gian cập nhật cuối | `"2025-09-30 10:30:45"` |

## 🔧 **Database Query:**

```sql
SELECT face_id, name, description, created_at, updated_at 
FROM faces 
ORDER BY created_at DESC
```

## 📈 **Use Cases:**

### ✅ **Successful Scenarios:**
- **Empty Database:** `{"success": true, "faces": [], "count": 0}`
- **With Data:** Trả về danh sách đầy đủ theo thứ tự mới nhất trước
- **Mixed Descriptions:** Một số có description, một số null

### ❌ **Error Scenarios:**
- Database connection failed
- SQL query error
- Permission denied

## 🌐 **Spring Boot Integration:**

**Mapping Response:**
```java
// Spring Boot sẽ nhận response này:
Map<String, Object> response = faceService.listRegisteredFaces();

// Có thể parse như sau:
List<Map<String, Object>> faces = (List<Map<String, Object>>) response.get("faces");
Integer count = (Integer) response.get("count");
Boolean success = (Boolean) response.get("success");
```

## 🧪 **Test Command:**

```bash
# Test endpoint
curl -X GET http://localhost:8000/api/v1/simple-face/list \
  -H "Content-Type: application/json"

# Expected response format matches exactly with Spring Boot expectation
```

## 📋 **Notes:**

- ✅ **Backward Compatible:** Format tương thích với Spring Boot controller
- ✅ **Sorted by Date:** Newest faces first (ORDER BY created_at DESC)  
- ✅ **Null Safe:** description có thể null
- ✅ **Consistent Format:** Same structure cho success và error cases