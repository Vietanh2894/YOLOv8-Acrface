#!/usr/bin/env python3
"""
🚀 FACE RECOGNITION API SERVER
Flask API để tích hợp với Java Spring Boot backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import cv2
import numpy as np
from PIL import Image
import io
import uuid
import logging
from datetime import datetime

from face_recognition_system import FaceRecognitionSystem

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Cho phép CORS từ Spring Boot

# Khởi tạo Face Recognition System
face_system = FaceRecognitionSystem()

# Thư mục lưu ảnh tạm
TEMP_FOLDER = 'temp_images'
os.makedirs(TEMP_FOLDER, exist_ok=True)

def save_base64_image(base64_string, filename):
    """
    Lưu ảnh từ base64 string
    
    Args:
        base64_string (str): Base64 string của ảnh
        filename (str): Tên file để lưu
    
    Returns:
        str: Đường dẫn file đã lưu
    """
    try:
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Tạo PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Lưu file
        filepath = os.path.join(TEMP_FOLDER, filename)
        image.save(filepath)
        
        return filepath
    except Exception as e:
        logger.error(f"Lỗi lưu ảnh base64: {e}")
        return None

def image_to_base64(image_path):
    """
    Chuyển ảnh thành base64 string
    
    Args:
        image_path (str): Đường dẫn ảnh
    
    Returns:
        str: Base64 string
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        logger.error(f"Lỗi chuyển ảnh thành base64: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """API kiểm tra trạng thái hệ thống"""
    try:
        total_faces = face_system.db_manager.get_total_faces()
        return jsonify({
            'status': 'OK',
            'message': 'Face Recognition API đang hoạt động',
            'timestamp': datetime.now().isoformat(),
            'total_registered_faces': total_faces,
            'version': '1.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Lỗi kiểm tra hệ thống: {str(e)}'
        }), 500

@app.route('/api/face/register', methods=['POST'])
def register_face():
    """
    API đăng ký khuôn mặt mới
    
    Body JSON:
    {
        "name": "Tên người",
        "image": "base64_string_của_ảnh" hoặc không có (dùng file upload),
        "description": "Mô tả (optional)"
    }
    
    Hoặc form-data:
    - name: Tên người
    - image: File ảnh
    """
    try:
        logger.info("Nhận request đăng ký khuôn mặt")
        
        # Lấy tên từ request
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            image_base64 = data.get('image')
            description = data.get('description', '')
        else:
            name = request.form.get('name')
            image_base64 = None
            description = request.form.get('description', '')
        
        if not name:
            return jsonify({
                'success': False,
                'message': 'Thiếu tham số name'
            }), 400
        
        # Xử lý ảnh
        image_path = None
        
        if image_base64:
            # Từ base64
            filename = f"register_{uuid.uuid4().hex}.jpg"
            image_path = save_base64_image(image_base64, filename)
        elif 'image' in request.files:
            # Từ file upload
            file = request.files['image']
            if file.filename != '':
                filename = f"register_{uuid.uuid4().hex}_{file.filename}"
                image_path = os.path.join(TEMP_FOLDER, filename)
                file.save(image_path)
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy ảnh trong request'
            }), 400
        
        # Đăng ký khuôn mặt
        result = face_system.register_face(image_path, name)
        
        # Xóa file tạm
        try:
            os.remove(image_path)
        except:
            pass
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Đăng ký khuôn mặt thành công',
                'data': {
                    'face_id': result['face_id'],
                    'person_name': result['person_name'],
                    'confidence': result.get('confidence', 0),
                    'embedding_dimension': result.get('embedding_shape', [512])[0] if 'embedding_shape' in result else 512,
                    'description': description
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"Lỗi đăng ký khuôn mặt: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/face/recognize', methods=['POST'])
def recognize_face():
    """
    API nhận diện khuôn mặt trong ảnh
    
    Body JSON:
    {
        "image": "base64_string_của_ảnh",
        "threshold": 0.6 (optional)
    }
    
    Hoặc form-data:
    - image: File ảnh
    - threshold: Ngưỡng similarity (optional)
    """
    try:
        logger.info("Nhận request nhận diện khuôn mặt")
        
        # Lấy threshold (optional)
        if request.is_json:
            data = request.get_json()
            image_base64 = data.get('image')
            threshold = data.get('threshold', 0.6)
        else:
            image_base64 = None
            threshold = float(request.form.get('threshold', 0.6))
        
        # Xử lý ảnh
        image_path = None
        
        if image_base64:
            # Từ base64
            filename = f"recognize_{uuid.uuid4().hex}.jpg"
            image_path = save_base64_image(image_base64, filename)
        elif 'image' in request.files:
            # Từ file upload
            file = request.files['image']
            if file.filename != '':
                filename = f"recognize_{uuid.uuid4().hex}_{file.filename}"
                image_path = os.path.join(TEMP_FOLDER, filename)
                file.save(image_path)
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy ảnh trong request'
            }), 400
        
        # Cập nhật threshold nếu cần
        original_threshold = face_system.face_processor.face_similarity_threshold
        if threshold != original_threshold:
            face_system.face_processor.face_similarity_threshold = threshold
        
        # Nhận diện khuôn mặt
        result = face_system.recognize_face(image_path)
        
        # Khôi phục threshold
        face_system.face_processor.face_similarity_threshold = original_threshold
        
        # Xóa file tạm
        try:
            os.remove(image_path)
        except:
            pass
        
        if result['success']:
            # Format lại kết quả cho API
            faces_data = []
            for i, match in enumerate(result['matches']):
                face_info = {
                    'face_index': i + 1,
                    'bounding_box': {
                        'x1': int(match['bbox'][0]),
                        'y1': int(match['bbox'][1]),
                        'x2': int(match['bbox'][2]),
                        'y2': int(match['bbox'][3])
                    },
                    'detection_confidence': float(match['confidence']),
                    'match_found': match['match_found'],
                    'best_similarity': float(match['best_similarity'])
                }
                
                if match['match_found']:
                    face_info.update({
                        'person_name': match['person_name'],
                        'match_similarity': float(match['match_similarity']),
                        'face_id': match.get('face_id', None)
                    })
                
                faces_data.append(face_info)
            
            return jsonify({
                'success': True,
                'message': f'Nhận diện thành công {result["total_faces"]} khuôn mặt',
                'data': {
                    'total_faces': result['total_faces'],
                    'threshold_used': threshold,
                    'faces': faces_data
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"Lỗi nhận diện khuôn mặt: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/face/compare', methods=['POST'])
def compare_faces():
    """
    API so sánh hai ảnh khuôn mặt
    
    Body JSON:
    {
        "image1": "base64_string_ảnh_1",
        "image2": "base64_string_ảnh_2", 
        "threshold": 0.6 (optional)
    }
    
    Hoặc form-data:
    - image1: File ảnh 1
    - image2: File ảnh 2
    - threshold: Ngưỡng similarity (optional)
    """
    try:
        logger.info("Nhận request so sánh khuôn mặt")
        
        # Lấy dữ liệu
        if request.is_json:
            data = request.get_json()
            image1_base64 = data.get('image1')
            image2_base64 = data.get('image2')
            threshold = data.get('threshold', 0.6)
        else:
            image1_base64 = None
            image2_base64 = None
            threshold = float(request.form.get('threshold', 0.6))
        
        # Xử lý ảnh 1
        image1_path = None
        if image1_base64:
            filename1 = f"compare1_{uuid.uuid4().hex}.jpg"
            image1_path = save_base64_image(image1_base64, filename1)
        elif 'image1' in request.files:
            file1 = request.files['image1']
            if file1.filename != '':
                filename1 = f"compare1_{uuid.uuid4().hex}_{file1.filename}"
                image1_path = os.path.join(TEMP_FOLDER, filename1)
                file1.save(image1_path)
        
        # Xử lý ảnh 2
        image2_path = None
        if image2_base64:
            filename2 = f"compare2_{uuid.uuid4().hex}.jpg"
            image2_path = save_base64_image(image2_base64, filename2)
        elif 'image2' in request.files:
            file2 = request.files['image2']
            if file2.filename != '':
                filename2 = f"compare2_{uuid.uuid4().hex}_{file2.filename}"
                image2_path = os.path.join(TEMP_FOLDER, filename2)
                file2.save(image2_path)
        
        if not image1_path or not image2_path:
            return jsonify({
                'success': False,
                'message': 'Cần cung cấp cả hai ảnh để so sánh'
            }), 400
        
        if not os.path.exists(image1_path) or not os.path.exists(image2_path):
            return jsonify({
                'success': False,
                'message': 'Không thể lưu ảnh từ request'
            }), 400
        
        # So sánh hai ảnh
        result = face_system.compare_two_images(image1_path, image2_path)
        
        # Xóa file tạm
        try:
            os.remove(image1_path)
            os.remove(image2_path)
        except:
            pass
        
        if result['success']:
            comparison = result['comparison']
            
            return jsonify({
                'success': True,
                'message': 'So sánh thành công',
                'data': {
                    'similarity': float(comparison['similarity']),
                    'is_same_person': comparison['is_same_person'],
                    'threshold': float(comparison['threshold']),
                    'confidence': float(comparison['confidence']),
                    'image1_info': {
                        'faces_count': result['image1']['faces_count'],
                        'detection_confidence': float(result['image1']['confidence'])
                    },
                    'image2_info': {
                        'faces_count': result['image2']['faces_count'],
                        'detection_confidence': float(result['image2']['confidence'])
                    }
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"Lỗi so sánh khuôn mặt: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/face/list', methods=['GET'])
def list_registered_faces():
    """API lấy danh sách tất cả khuôn mặt đã đăng ký"""
    try:
        embeddings = face_system.db_manager.get_all_face_embeddings()
        
        faces_list = []
        for emb in embeddings:
            faces_list.append({
                'face_id': emb['id'],
                'name': emb['name'],
                'embedding_dimension': len(emb['embedding'])
            })
        
        return jsonify({
            'success': True,
            'message': f'Tìm thấy {len(faces_list)} khuôn mặt đã đăng ký',
            'data': {
                'total_faces': len(faces_list),
                'faces': faces_list
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi lấy danh sách khuôn mặt: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/face/delete/<int:face_id>', methods=['DELETE'])
def delete_face(face_id):
    """API xóa khuôn mặt theo ID"""
    try:
        success = face_system.db_manager.delete_face_by_id(face_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Đã xóa khuôn mặt ID {face_id}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Không tìm thấy khuôn mặt ID {face_id}'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi xóa khuôn mặt {face_id}: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'API endpoint không tồn tại'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Lỗi server nội bộ'
    }), 500

if __name__ == '__main__':
    print("🚀 FACE RECOGNITION API SERVER")
    print("=" * 50)
    print("📡 Các API endpoints:")
    print("  • GET  /api/health           - Kiểm tra trạng thái")
    print("  • POST /api/face/register    - Đăng ký khuôn mặt")
    print("  • POST /api/face/recognize   - Nhận diện khuôn mặt")
    print("  • POST /api/face/compare     - So sánh hai ảnh")
    print("  • GET  /api/face/list        - Danh sách đã đăng ký")
    print("  • DEL  /api/face/delete/<id> - Xóa khuôn mặt")
    print("=" * 50)
    print("🌐 Server đang chạy tại: http://localhost:5000")
    print("📖 Xem API docs: http://localhost:5000/api/health")
    
    app.run(
        host='0.0.0.0',  # Cho phép truy cập từ bên ngoài
        port=5000,       # Port 5000
        debug=True       # Debug mode
    )