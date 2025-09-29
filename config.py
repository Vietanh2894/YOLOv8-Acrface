# Face Recognition System Configuration

# Database Configuration
DB_HOST = '127.0.0.1'   # change to your server
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = '123456'
DB_NAME = 'smartparking'

# Face Recognition Configuration
FACE_DETECTION_CONFIDENCE = 0.5  # YOLOv8 detection confidence threshold
FACE_SIMILARITY_THRESHOLD = 0.6  # Cosine similarity threshold for face matching
EMBEDDING_DIMENSION = 512         # ArcFace embedding dimension

# Image Processing Configuration
INPUT_IMAGE_SIZE = (640, 640)    # YOLOv8 input size
FACE_CROP_SIZE = (112, 112)      # ArcFace input size

# Paths
YOLO_MODEL_PATH = "yolov8n-face.pt"  # YOLOv8 face model path
TEST_IMAGE_1 = r"C:\Users\ADMIN\Documents\NGHIENCUUKHOAHOC\insightface\test11.jpg"
TEST_IMAGE_2 = r"C:\Users\ADMIN\Documents\NGHIENCUUKHOAHOC\insightface\test13.jpg"