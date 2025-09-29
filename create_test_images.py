import cv2
import numpy as np

# Tạo ảnh test đơn giản (thay thế cho ảnh thật)
def create_test_image(filename, text="Test Face"):
    # Tạo ảnh trắng 400x400
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Vẽ một "khuôn mặt" đơn giản
    # Mặt (hình tròn)
    cv2.circle(img, (200, 200), 100, (200, 180, 160), -1)
    
    # Mắt
    cv2.circle(img, (170, 180), 15, (0, 0, 0), -1)
    cv2.circle(img, (230, 180), 15, (0, 0, 0), -1)
    
    # Mũi
    cv2.circle(img, (200, 200), 5, (150, 120, 100), -1)
    
    # Miệng
    cv2.ellipse(img, (200, 230), (25, 15), 0, 0, 180, (100, 50, 50), -1)
    
    # Text
    cv2.putText(img, text, (150, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Lưu ảnh
    cv2.imwrite(filename, img)
    print(f"Đã tạo ảnh test: {filename}")

if __name__ == "__main__":
    # Tạo 2 ảnh test
    create_test_image("test1.png", "Person 1")
    create_test_image("test2.png", "Person 2")
    
    print("✅ Đã tạo xong 2 ảnh test!")
    print("📝 Lưu ý: Đây chỉ là ảnh test đơn giản.")
    print("📷 Để test thực tế, hãy thay bằng ảnh khuôn mặt thật.")