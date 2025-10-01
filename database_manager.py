import pymysql
import json
import numpy as np
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Kết nối đến MySQL database"""
        try:
            self.connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                charset='utf8mb4',
                autocommit=True
            )
            logger.info("Đã kết nối thành công đến database")
        except Exception as e:
            logger.error(f"Lỗi kết nối database: {e}")
            raise
    
    def create_table(self):
        """Tạo bảng faces nếu chưa tồn tại"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS faces (
            face_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            embedding JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
            logger.info("Đã tạo/kiểm tra bảng faces thành công")
        except Exception as e:
            logger.error(f"Lỗi tạo bảng: {e}")
            raise
    
    def save_face_embedding(self, name, embedding, description=None):
        """
        Lưu embedding của khuôn mặt vào database
        
        Args:
            name (str): Tên của người
            embedding (np.ndarray): Vector embedding 512 chiều
            description (str, optional): Mô tả thêm về người này
        
        Returns:
            int: ID của record được tạo
        """
        try:
            # Chuyển numpy array thành list để lưu JSON
            embedding_list = embedding.tolist()
            embedding_json = json.dumps(embedding_list)
            
            insert_query = """
            INSERT INTO faces (name, description, embedding) VALUES (%s, %s, %s)
            """
            
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query, (name, description, embedding_json))
                face_id = cursor.lastrowid
            
            logger.info(f"Đã lưu embedding cho {name} với ID: {face_id}")
            return face_id
        
        except Exception as e:
            logger.error(f"Lỗi lưu embedding: {e}")
            raise
    
    def get_all_face_embeddings(self):
        """
        Lấy tất cả embedding từ database
        
        Returns:
            list: Danh sách dict {'id', 'name', 'description', 'embedding'}
        """
        try:
            select_query = "SELECT face_id, name, description, embedding FROM faces"
            
            with self.connection.cursor() as cursor:
                cursor.execute(select_query)
                results = cursor.fetchall()
            
            # Chuyển JSON string thành numpy array
            face_data = []
            for result in results:
                face_id, name, description, embedding_json = result[0], result[1], result[2], result[3]
                embedding_list = json.loads(embedding_json)
                embedding = np.array(embedding_list, dtype=np.float32)
                face_data.append({
                    'id': face_id, 
                    'name': name, 
                    'description': description, 
                    'embedding': embedding
                })
            
            logger.info(f"Đã lấy {len(face_data)} embedding từ database")
            return face_data
        
        except Exception as e:
            logger.error(f"Lỗi lấy embedding: {e}")
            return []
    
    def get_total_faces(self):
        """
        Lấy tổng số khuôn mặt trong database
        
        Returns:
            int: Số lượng khuôn mặt
        """
        try:
            count_query = "SELECT COUNT(*) FROM faces"
            
            with self.connection.cursor() as cursor:
                cursor.execute(count_query)
                result = cursor.fetchone()
                return result[0] if result else 0
            
        except Exception as e:
            logger.error(f"Lỗi đếm faces: {e}")
            return 0
    
    def get_face_by_name(self, name):
        """
        Lấy embedding theo tên
        
        Args:
            name (str): Tên cần tìm
        
        Returns:
            tuple: (face_id, name, description, embedding) hoặc None nếu không tìm thấy
        """
        try:
            select_query = "SELECT face_id, name, description, embedding FROM faces WHERE name = %s"
            
            with self.connection.cursor() as cursor:
                cursor.execute(select_query, (name,))
                result = cursor.fetchone()
            
            if result:
                face_id, name, description, embedding_json = result
                embedding_list = json.loads(embedding_json)
                embedding = np.array(embedding_list, dtype=np.float32)
                return (face_id, name, description, embedding)
            
            return None
        
        except Exception as e:
            logger.error(f"Lỗi tìm kiếm theo tên: {e}")
            return None
    
    def update_face_embedding(self, face_id, name, embedding, description=None):
        """
        Cập nhật embedding cho một face ID
        
        Args:
            face_id (int): ID của face
            name (str): Tên mới
            embedding (np.ndarray): Embedding mới
            description (str, optional): Mô tả mới
        
        Returns:
            bool: True nếu cập nhật thành công
        """
        try:
            embedding_list = embedding.tolist()
            embedding_json = json.dumps(embedding_list)
            
            update_query = """
            UPDATE faces SET name = %s, description = %s, embedding = %s 
            WHERE face_id = %s
            """
            
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(update_query, (name, description, embedding_json, face_id))
            
            if affected_rows > 0:
                logger.info(f"Đã cập nhật embedding cho ID: {face_id}")
                return True
            else:
                logger.warning(f"Không tìm thấy face ID: {face_id}")
                return False
        
        except Exception as e:
            logger.error(f"Lỗi cập nhật embedding: {e}")
            return False
    
    def delete_face(self, face_id):
        """
        Xóa face theo ID
        
        Args:
            face_id (int): ID của face cần xóa
        
        Returns:
            bool: True nếu xóa thành công
        """
        try:
            delete_query = "DELETE FROM faces WHERE face_id = %s"
            
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(delete_query, (face_id,))
            
            if affected_rows > 0:
                logger.info(f"Đã xóa face ID: {face_id}")
                return True
            else:
                logger.warning(f"Không tìm thấy face ID: {face_id}")
                return False
        
        except Exception as e:
            logger.error(f"Lỗi xóa face: {e}")
            return False
    
    def get_all_faces(self):
        """
        Lấy thông tin cơ bản của tất cả faces (không bao gồm embedding)
        
        Returns:
            list: Danh sách tuple (face_id, name, description, created_at, updated_at)
        """
        try:
            select_query = "SELECT face_id, name, description, created_at, updated_at FROM faces ORDER BY created_at DESC"
            
            with self.connection.cursor() as cursor:
                cursor.execute(select_query)
                results = cursor.fetchall()
            
            logger.info(f"Đã lấy thông tin {len(results)} faces từ database")
            return results
        
        except Exception as e:
            logger.error(f"Lỗi lấy danh sách faces: {e}")
            return []

    def get_face_by_id(self, face_id):
        """
        Lấy thông tin face theo ID
        
        Args:
            face_id (int): ID của face cần tìm
        
        Returns:
            tuple: (face_id, name, description, created_at, updated_at) hoặc None
        """
        try:
            select_query = "SELECT face_id, name, description, created_at, updated_at FROM faces WHERE face_id = %s"
            
            with self.connection.cursor() as cursor:
                cursor.execute(select_query, (face_id,))
                result = cursor.fetchone()
            
            return result
        
        except Exception as e:
            logger.error(f"Lỗi tìm face theo ID: {e}")
            return None

    def close(self):
        """Đóng kết nối database"""
        if self.connection:
            self.connection.close()
            logger.info("Đã đóng kết nối database")

if __name__ == "__main__":
    # Test database connection and operations
    db = DatabaseManager()
    
    # Test tạo một embedding giả
    test_embedding = np.random.rand(512).astype(np.float32)
    
    # Test save
    face_id = db.save_face_embedding("Test User", test_embedding)
    print(f"Saved face with ID: {face_id}")
    
    # Test get all
    all_faces = db.get_all_face_embeddings()
    print(f"Total faces in DB: {len(all_faces)}")
    
    # Test get by name
    face = db.get_face_by_name("Test User")
    if face:
        print(f"Found face: {face[1]} with ID: {face[0]}")
    
    db.close()