import cv2
import numpy as np
from ultralytics import YOLO
import insightface
from insightface.app import FaceAnalysis
import logging
from config import (
    FACE_DETECTION_CONFIDENCE, 
    FACE_SIMILARITY_THRESHOLD,
    EMBEDDING_DIMENSION,
    INPUT_IMAGE_SIZE,
    FACE_CROP_SIZE
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaceProcessor:
    def __init__(self, yolo_model_path=None):
        """
        Khởi tạo Face Processor với YOLOv8 và InsightFace
        
        Args:
            yolo_model_path (str): Đường dẫn đến YOLO model, nếu None sẽ dùng YOLOv8n
        """
        self.face_detection_confidence = FACE_DETECTION_CONFIDENCE
        self.face_similarity_threshold = FACE_SIMILARITY_THRESHOLD
        
        # Khởi tạo YOLO model
        try:
            if yolo_model_path and os.path.exists(yolo_model_path):
                self.yolo_model = YOLO(yolo_model_path)
                logger.info(f"Đã tải YOLO model từ: {yolo_model_path}")
            else:
                # Sử dụng YOLOv8n mặc định để detect person, sau đó crop face region
                self.yolo_model = YOLO('yolov8n.pt')
                logger.info("Đã tải YOLOv8n model mặc định")
        except Exception as e:
            logger.error(f"Lỗi tải YOLO model: {e}")
            raise
        
        # Khởi tạo InsightFace
        try:
            self.face_app = FaceAnalysis(providers=['CPUExecutionProvider'])
            self.face_app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("Đã khởi tạo InsightFace thành công")
        except Exception as e:
            logger.error(f"Lỗi khởi tạo InsightFace: {e}")
            raise
    
    def detect_faces_yolo(self, image):
        """
        Sử dụng YOLO để detect người và crop vùng có thể có mặt
        
        Args:
            image (np.ndarray): Ảnh đầu vào
        
        Returns:
            list: Danh sách các bounding box có thể chứa face
        """
        try:
            # YOLOv8 detect person (class 0)
            results = self.yolo_model(image, conf=self.face_detection_confidence)
            
            person_boxes = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Class 0 là person trong COCO dataset
                        if int(box.cls) == 0:  # person class
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            confidence = float(box.conf[0])
                            
                            # Crop vùng upper body để tìm face (khoảng 30% trên cùng)
                            height = y2 - y1
                            face_y1 = y1
                            face_y2 = y1 + height * 0.4  # 40% phần trên của person
                            
                            person_boxes.append({
                                'bbox': [int(x1), int(face_y1), int(x2), int(face_y2)],
                                'confidence': confidence
                            })
            
            return person_boxes
            
        except Exception as e:
            logger.error(f"Lỗi detect với YOLO: {e}")
            return []
    
    def extract_face_embedding(self, image):
        """
        Trích xuất embedding từ ảnh sử dụng InsightFace
        
        Args:
            image (np.ndarray): Ảnh đầu vào
        
        Returns:
            list: Danh sách các dict chứa face info và embedding
        """
        try:
            faces = self.face_app.get(image)
            
            face_data = []
            for face in faces:
                if face.embedding is not None:
                    # Normalize embedding
                    embedding = face.normed_embedding
                    
                    face_info = {
                        'bbox': face.bbox.astype(int).tolist(),
                        'embedding': embedding,
                        'confidence': float(face.det_score) if hasattr(face, 'det_score') else 1.0,
                        'landmarks': face.kps.astype(int).tolist() if face.kps is not None else None
                    }
                    face_data.append(face_info)
            
            logger.info(f"Đã trích xuất {len(face_data)} face embeddings")
            return face_data
            
        except Exception as e:
            logger.error(f"Lỗi trích xuất embedding: {e}")
            return []
    
    def process_image(self, image_path):
        """
        Xử lý ảnh hoàn chỉnh: detect faces và extract embeddings
        
        Args:
            image_path (str): Đường dẫn đến ảnh
        
        Returns:
            dict: Kết quả xử lý bao gồm face info và embeddings
        """
        try:
            # Đọc ảnh
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Không thể đọc ảnh: {image_path}")
                return None
            
            # Chuyển sang RGB cho InsightFace
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Extract faces và embeddings trực tiếp với InsightFace
            face_data = self.extract_face_embedding(image_rgb)
            
            result = {
                'image_path': image_path,
                'image_shape': image.shape,
                'faces': face_data,
                'total_faces': len(face_data)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi xử lý ảnh {image_path}: {e}")
            return None
    
    @staticmethod
    def calculate_cosine_similarity(embedding1, embedding2):
        """
        Tính cosine similarity giữa 2 embeddings
        
        Args:
            embedding1 (np.ndarray): Embedding thứ nhất
            embedding2 (np.ndarray): Embedding thứ hai
        
        Returns:
            float: Giá trị cosine similarity
        """
        try:
            # Normalize embeddings
            embedding1 = embedding1 / np.linalg.norm(embedding1)
            embedding2 = embedding2 / np.linalg.norm(embedding2)
            
            # Tính cosine similarity
            similarity = np.dot(embedding1, embedding2)
            return float(similarity)
        
        except Exception as e:
            logger.error(f"Lỗi tính cosine similarity: {e}")
            return 0.0
    
    def compare_faces(self, embedding1, embedding2, threshold=None):
        """
        So sánh 2 faces và xác định có phải cùng người không
        
        Args:
            embedding1 (np.ndarray): Embedding thứ nhất
            embedding2 (np.ndarray): Embedding thứ hai
            threshold (float): Ngưỡng similarity, nếu None sử dụng config
        
        Returns:
            dict: Kết quả so sánh
        """
        if threshold is None:
            threshold = self.face_similarity_threshold
        
        similarity = self.calculate_cosine_similarity(embedding1, embedding2)
        is_same_person = similarity >= threshold
        
        return {
            'similarity': similarity,
            'is_same_person': is_same_person,
            'threshold': threshold,
            'confidence': abs(similarity - threshold)
        }
    
    def find_matching_face(self, query_embedding, database_embeddings, threshold=None):
        """
        Tìm face matching trong database
        
        Args:
            query_embedding (np.ndarray): Embedding cần tìm
            database_embeddings (list): List các tuple (id, name, embedding)
            threshold (float): Ngưỡng similarity
        
        Returns:
            dict: Kết quả tìm kiếm
        """
        if threshold is None:
            threshold = self.face_similarity_threshold
        
        best_match = None
        best_similarity = 0.0
        
        for db_face in database_embeddings:
            face_id = db_face['id']
            name = db_face['name']  
            db_embedding = db_face['embedding']
            
            similarity = self.calculate_cosine_similarity(query_embedding, db_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                if similarity >= threshold:
                    best_match = {
                        'id': face_id,
                        'name': name,
                        'similarity': similarity,
                        'confidence': similarity - threshold
                    }
        
        return {
            'best_match': best_match,
            'best_similarity': best_similarity,
            'threshold': threshold,
            'found_match': best_match is not None
        }

import os

if __name__ == "__main__":
    # Test face processor
    processor = FaceProcessor()
    
    # Test với ảnh mẫu
    test_image = r"C:\Users\ADMIN\Documents\NGHIENCUUKHOAHOC\insightface\test1.png"
    
    if os.path.exists(test_image):
        result = processor.process_image(test_image)
        if result:
            print(f"Đã xử lý ảnh: {result['image_path']}")
            print(f"Tìm thấy {result['total_faces']} khuôn mặt")
            
            for i, face in enumerate(result['faces']):
                print(f"Face {i+1}: confidence={face['confidence']:.3f}, embedding_shape={face['embedding'].shape}")
    else:
        print(f"Không tìm thấy ảnh test: {test_image}")