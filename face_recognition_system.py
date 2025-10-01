import cv2
import numpy as np
import os
from face_processor import FaceProcessor
from database_manager import DatabaseManager
import logging
from config import TEST_IMAGE_1, TEST_IMAGE_2

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FaceRecognitionSystem:
    def __init__(self):
        """Khởi tạo hệ thống nhận diện khuôn mặt"""
        self.face_processor = FaceProcessor()
        self.db_manager = DatabaseManager()
        logger.info("Đã khởi tạo Face Recognition System")
    
    def register_face_from_base64(self, base64_image, person_name, description=None):
        """
        Đăng ký khuôn mặt từ base64 image
        
        Args:
            base64_image (str): Base64 encoded image
            person_name (str): Tên của người
            description (str, optional): Mô tả thêm về người này
        
        Returns:
            dict: Kết quả đăng ký
        """
        import tempfile
        import base64
        from PIL import Image
        from io import BytesIO
        
        try:
            # Decode base64 to image
            if base64_image.startswith('data:image'):
                base64_image = base64_image.split(',')[1]
            
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                image.save(temp_file.name, 'JPEG')
                temp_path = temp_file.name
            
            # Use existing register_face method
            result = self.register_face(temp_path, person_name, description)
            
            # Clean up temp file
            import os
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi đăng ký từ base64: {e}")
            return {
                'success': False,
                'message': f'Lỗi xử lý ảnh base64: {str(e)}',
                'face_count': 0
            }

    def recognize_face_from_base64(self, base64_image, threshold=0.6):
        """
        Nhận diện khuôn mặt từ base64 image
        
        Args:
            base64_image (str): Base64 encoded image
            threshold (float): Ngưỡng similarity
        
        Returns:
            dict: Kết quả nhận diện
        """
        import tempfile
        import base64
        from PIL import Image
        from io import BytesIO
        
        try:
            # Decode base64 to image
            if base64_image.startswith('data:image'):
                base64_image = base64_image.split(',')[1]
            
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                image.save(temp_file.name, 'JPEG')
                temp_path = temp_file.name
            
            # Process image and extract embedding
            face_result = self.face_processor.process_image(temp_path)
            
            # Clean up temp file
            import os
            os.unlink(temp_path)
            
            if not face_result or face_result['total_faces'] == 0:
                return {
                    'success': False,
                    'message': 'Không tìm thấy khuôn mặt trong ảnh',
                    'name': None,
                    'face_id': None,
                    'similarity': None
                }
            
            logger.info(f"Đã xử lý {face_result['total_faces']} khuôn mặt trong ảnh")

            # Get database embeddings
            database_embeddings = self.db_manager.get_all_face_embeddings()
            logger.info(f"Database có {len(database_embeddings)} khuôn mặt")
            
            if not database_embeddings:
                return {
                    'success': True,
                    'message': 'Database trống, chưa có khuôn mặt nào được đăng ký',
                    'name': None,
                    'face_id': None,
                    'similarity': None
                }
            
            # Get first face embedding
            face_embedding = face_result['faces'][0]['embedding']
            logger.info(f"Query embedding shape: {face_embedding.shape}")
            
            # Debug: Log database embeddings info
            for i, db_face in enumerate(database_embeddings):
                logger.info(f"DB face {i}: id={db_face['id']}, name={db_face['name']}, embedding_shape={db_face['embedding'].shape}")
            
            # Find matching face with custom threshold
            match_result = self.face_processor.find_matching_face(
                face_embedding, 
                database_embeddings,
                threshold=threshold
            )
            
            logger.info(f"Match result: best_similarity={match_result['best_similarity']:.4f}, threshold={threshold}, found_match={match_result['found_match']}")
            
            if match_result['found_match'] and match_result['best_match']:
                logger.info(f"FOUND MATCH: {match_result['best_match']['name']} (similarity: {match_result['best_match']['similarity']:.4f})")
                return {
                    'success': True,
                    'message': f'Nhận diện thành công: {match_result["best_match"]["name"]}',
                    'name': match_result['best_match']['name'],
                    'face_id': match_result['best_match']['id'],
                    'similarity': match_result['best_match']['similarity'],
                    'confidence': match_result['best_match']['confidence']
                }
            else:
                logger.info(f"NO MATCH FOUND: best_similarity={match_result['best_similarity']:.4f} < threshold={threshold}")
                # Thêm debug cho similarity values
                similarities = []
                for db_face in database_embeddings:
                    sim = self.face_processor.calculate_cosine_similarity(face_embedding, db_face['embedding'])
                    similarities.append(f"{db_face['name']}={sim:.4f}")
                logger.info(f"All similarities: {', '.join(similarities)}")
                
                return {
                    'success': True,
                    'message': f'Không tìm thấy khuôn mặt phù hợp (best similarity: {match_result["best_similarity"]:.4f} < threshold: {threshold})',
                    'name': None,
                    'face_id': None,
                    'similarity': match_result['best_similarity'],
                    'confidence': None,
                    'debug_similarities': similarities
                }
            
        except Exception as e:
            logger.error(f"Lỗi nhận diện từ base64: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'message': f'Lỗi xử lý ảnh base64: {str(e)}'
            }

    def compare_faces_from_base64(self, base64_image1, base64_image2, threshold=0.6):
        """
        So sánh 2 khuôn mặt từ base64 images
        
        Args:
            base64_image1 (str): Base64 encoded first image
            base64_image2 (str): Base64 encoded second image
            threshold (float): Ngưỡng similarity
        
        Returns:
            dict: Kết quả so sánh
        """
        import tempfile
        import base64
        from PIL import Image
        from io import BytesIO
        
        try:
            # Decode base64 images
            if base64_image1.startswith('data:image'):
                base64_image1 = base64_image1.split(',')[1]
            if base64_image2.startswith('data:image'):
                base64_image2 = base64_image2.split(',')[1]
            
            image1_data = base64.b64decode(base64_image1)
            image2_data = base64.b64decode(base64_image2)
            
            image1 = Image.open(BytesIO(image1_data))
            image2 = Image.open(BytesIO(image2_data))
            
            # Save to temporary files
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file1:
                image1.save(temp_file1.name, 'JPEG')
                temp_path1 = temp_file1.name
                
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file2:
                image2.save(temp_file2.name, 'JPEG')
                temp_path2 = temp_file2.name
            
            # Use existing compare method
            result = self.compare_two_images(temp_path1, temp_path2)
            
            # Clean up temp files
            import os
            os.unlink(temp_path1)
            os.unlink(temp_path2)
            
            # Extract comparison data and format for FastAPI
            if result['success'] and result.get('comparison'):
                comparison = result['comparison']
                similarity = comparison.get('similarity')
                is_match = comparison.get('is_same_person', False)
                
                logger.info(f"Comparison successful: similarity={similarity:.4f}, match={is_match}")
                
                return {
                    'success': True,
                    'message': f'So sánh thành công (similarity: {similarity:.4f})',
                    'similarity': float(similarity),
                    'match': bool(is_match)
                }
            else:
                logger.error(f"Comparison failed: {result.get('message', 'Unknown error')}")
                return {
                    'success': False,
                    'message': result.get('message', 'Lỗi so sánh không xác định'),
                    'similarity': None,
                    'match': None
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Lỗi so sánh từ base64: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'message': f'Lỗi xử lý ảnh base64: {str(e)}',
                'similarity': None,
                'match': None
            }

    def register_face(self, image_path, person_name, description=None):
        """
        Đăng ký khuôn mặt mới vào hệ thống
        
        Args:
            image_path (str): Đường dẫn đến ảnh
            person_name (str): Tên của người
            description (str, optional): Mô tả thêm về người này
        
        Returns:
            dict: Kết quả đăng ký
        """
        try:
            # Xử lý ảnh và trích xuất embedding
            result = self.face_processor.process_image(image_path)
            
            if not result or result['total_faces'] == 0:
                return {
                    'success': False,
                    'message': 'Không tìm thấy khuôn mặt trong ảnh',
                    'face_count': 0
                }
            
            if result['total_faces'] > 1:
                logger.warning(f"Tìm thấy {result['total_faces']} khuôn mặt, chỉ sử dụng khuôn mặt đầu tiên")
            
            # Lấy embedding của khuôn mặt đầu tiên
            face_embedding = result['faces'][0]['embedding']
            face_confidence = result['faces'][0]['confidence']
            
            # Lưu vào database
            face_id = self.db_manager.save_face_embedding(person_name, face_embedding, description)
            
            return {
                'success': True,
                'message': f'Đã đăng ký thành công khuôn mặt cho {person_name}',
                'face_id': face_id,
                'person_name': person_name,
                'description': description,
                'face_count': result['total_faces'],
                'confidence': face_confidence,
                'embedding_shape': face_embedding.shape
            }
        
        except Exception as e:
            logger.error(f"Lỗi đăng ký khuôn mặt: {e}")
            return {
                'success': False,
                'message': f'Lỗi đăng ký: {str(e)}',
                'face_count': 0
            }
    
    def recognize_face(self, image_path):
        """
        Nhận diện khuôn mặt từ ảnh
        
        Args:
            image_path (str): Đường dẫn đến ảnh
        
        Returns:
            dict: Kết quả nhận diện
        """
        try:
            # Xử lý ảnh và trích xuất embedding
            result = self.face_processor.process_image(image_path)
            
            if not result or result['total_faces'] == 0:
                return {
                    'success': False,
                    'message': 'Không tìm thấy khuôn mặt trong ảnh',
                    'matches': []
                }
            
            # Lấy tất cả embeddings từ database
            database_embeddings = self.db_manager.get_all_face_embeddings()
            
            if not database_embeddings:
                return {
                    'success': False,
                    'message': 'Database trống, chưa có khuôn mặt nào được đăng ký',
                    'matches': []
                }
            
            # Nhận diện từng khuôn mặt trong ảnh
            matches = []
            for i, face in enumerate(result['faces']):
                face_embedding = face['embedding']
                
                # Tìm matching face trong database
                match_result = self.face_processor.find_matching_face(
                    face_embedding, 
                    database_embeddings
                )
                
                face_match = {
                    'face_index': i,
                    'bbox': face['bbox'],
                    'confidence': face['confidence'],
                    'match_found': match_result['found_match'],
                    'best_similarity': match_result['best_similarity'],
                    'threshold': match_result['threshold']
                }
                
                if match_result['best_match']:
                    face_match.update({
                        'person_id': match_result['best_match']['id'],
                        'person_name': match_result['best_match']['name'],
                        'match_similarity': match_result['best_match']['similarity'],
                        'match_confidence': match_result['best_match']['confidence']
                    })
                else:
                    face_match.update({
                        'person_id': None,
                        'person_name': 'Unknown',
                        'match_similarity': match_result['best_similarity'],
                        'match_confidence': 0.0
                    })
                
                matches.append(face_match)
            
            return {
                'success': True,
                'message': f'Đã xử lý {len(matches)} khuôn mặt',
                'total_faces': result['total_faces'],
                'matches': matches,
                'image_path': image_path
            }
        
        except Exception as e:
            logger.error(f"Lỗi nhận diện khuôn mặt: {e}")
            return {
                'success': False,
                'message': f'Lỗi nhận diện: {str(e)}',
                'matches': []
            }
    
    def compare_two_images(self, image1_path, image2_path):
        """
        So sánh khuôn mặt giữa 2 ảnh
        
        Args:
            image1_path (str): Đường dẫn ảnh thứ nhất
            image2_path (str): Đường dẫn ảnh thứ hai
        
        Returns:
            dict: Kết quả so sánh
        """
        try:
            # Xử lý ảnh 1
            result1 = self.face_processor.process_image(image1_path)
            if not result1 or result1['total_faces'] == 0:
                return {
                    'success': False,
                    'message': f'Không tìm thấy khuôn mặt trong ảnh {image1_path}',
                    'comparison': None
                }
            
            # Xử lý ảnh 2
            result2 = self.face_processor.process_image(image2_path)
            if not result2 or result2['total_faces'] == 0:
                return {
                    'success': False,
                    'message': f'Không tìm thấy khuôn mặt trong ảnh {image2_path}',
                    'comparison': None
                }
            
            # Lấy embedding của khuôn mặt đầu tiên từ mỗi ảnh
            embedding1 = result1['faces'][0]['embedding']
            embedding2 = result2['faces'][0]['embedding']
            
            # So sánh
            comparison = self.face_processor.compare_faces(embedding1, embedding2)
            
            return {
                'success': True,
                'message': 'So sánh thành công',
                'image1': {
                    'path': image1_path,
                    'faces_count': result1['total_faces'],
                    'confidence': result1['faces'][0]['confidence']
                },
                'image2': {
                    'path': image2_path,
                    'faces_count': result2['total_faces'],
                    'confidence': result2['faces'][0]['confidence']
                },
                'comparison': comparison
            }
        
        except Exception as e:
            logger.error(f"Lỗi so sánh ảnh: {e}")
            return {
                'success': False,
                'message': f'Lỗi so sánh: {str(e)}',
                'comparison': None
            }
    
    def visualize_results(self, image_path, recognition_result):
        """
        Vẽ bounding box và kết quả nhận diện lên ảnh
        
        Args:
            image_path (str): Đường dẫn ảnh
            recognition_result (dict): Kết quả nhận diện
        
        Returns:
            np.ndarray: Ảnh với annotations
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            if not recognition_result['success']:
                return image
            
            for match in recognition_result['matches']:
                bbox = match['bbox']
                x1, y1, x2, y2 = bbox
                
                # Màu: xanh lá nếu nhận diện được, đỏ nếu không
                color = (0, 255, 0) if match['match_found'] else (0, 0, 255)
                
                # Vẽ bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                # Text thông tin
                if match['match_found']:
                    label = f"{match['person_name']} ({match['match_similarity']:.3f})"
                else:
                    label = f"Unknown ({match['best_similarity']:.3f})"
                
                # Vẽ text
                font_scale = 0.6
                font_thickness = 2
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
                
                # Background cho text
                cv2.rectangle(image, (x1, y1 - text_size[1] - 10), 
                            (x1 + text_size[0], y1), color, -1)
                
                # Text
                cv2.putText(image, label, (x1, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
            
            return image
        
        except Exception as e:
            logger.error(f"Lỗi visualize: {e}")
            return None
    
    def close(self):
        """Đóng các kết nối"""
        self.db_manager.close()
        logger.info("Đã đóng Face Recognition System")

def print_result(result, title="Kết quả"):
    """In kết quả đẹp"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    
    if result['success']:
        print(f"✅ {result['message']}")
        if 'comparison' in result and result['comparison']:
            comp = result['comparison']
            print(f"🔍 Similarity: {comp['similarity']:.4f}")
            print(f"🎯 Threshold: {comp['threshold']:.4f}")
            print(f"👥 Same Person: {'YES' if comp['is_same_person'] else 'NO'}")
            print(f"📊 Confidence: {comp['confidence']:.4f}")
        
        if 'matches' in result:
            for i, match in enumerate(result['matches']):
                print(f"\n--- Face {i+1} ---")
                print(f"👤 Person: {match['person_name']}")
                print(f"🎯 Similarity: {match['match_similarity']:.4f}")
                print(f"✨ Match: {'YES' if match['match_found'] else 'NO'}")
    else:
        print(f"❌ {result['message']}")

if __name__ == "__main__":
    # Test hệ thống
    system = FaceRecognitionSystem()
    
    print("🚀 Bắt đầu test Face Recognition System")
    
    # Test 1: Đăng ký khuôn mặt từ ảnh đầu tiên
    if os.path.exists(TEST_IMAGE_1):
        print(f"\n📸 Đăng ký khuôn mặt từ: {TEST_IMAGE_1}")
        register_result = system.register_face(TEST_IMAGE_1, "Người test 12")
        print_result(register_result, "Kết quả đăng ký")
    
    # Test 2: Nhận diện khuôn mặt từ ảnh thứ hai
    if os.path.exists(TEST_IMAGE_2):
        print(f"\n🔍 Nhận diện khuôn mặt từ: {TEST_IMAGE_2}")
        recognize_result = system.recognize_face(TEST_IMAGE_2)
        print_result(recognize_result, "Kết quả nhận diện")
    
    # Test 3: So sánh trực tiếp 2 ảnh
    if os.path.exists(TEST_IMAGE_1) and os.path.exists(TEST_IMAGE_2):
        print(f"\n⚖️ So sánh 2 ảnh:")
        print(f"   Ảnh 1: {TEST_IMAGE_1}")
        print(f"   Ảnh 2: {TEST_IMAGE_2}")
        compare_result = system.compare_two_images(TEST_IMAGE_1, TEST_IMAGE_2)
        print_result(compare_result, "Kết quả so sánh")
        
        # Visualize kết quả
        if compare_result['success'] and recognize_result['success']:
            annotated_img = system.visualize_results(TEST_IMAGE_2, recognize_result)
            if annotated_img is not None:
                output_path = "result_annotated.jpg"
                cv2.imwrite(output_path, annotated_img)
                print(f"💾 Đã lưu ảnh kết quả: {output_path}")
    
    system.close()
    print("\n✅ Hoàn thành test!")