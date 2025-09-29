#!/usr/bin/env python3
"""
Script đổi tên field id thành face_id trong table faces
"""

import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

def rename_column():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            charset='utf8mb4'
        )

        with connection.cursor() as cursor:
            print("🔄 Đang đổi tên column 'id' thành 'face_id'...")
            
            # Câu lệnh ALTER TABLE để đổi tên column
            sql = """
            ALTER TABLE faces 
            CHANGE COLUMN id face_id INT AUTO_INCREMENT
            """
            
            cursor.execute(sql)
            connection.commit()
            
            print("✅ Đã đổi tên thành công!")
            
            # Kiểm tra lại cấu trúc table
            print("\n📊 CẤU TRÚC TABLE 'faces' SAU KHI ĐỔI TÊN:")
            cursor.execute("DESCRIBE faces;")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  • {col[0]} ({col[1]})")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("💡 Có thể column đã được đổi tên trước đó")
    
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    print("🔧 ĐỔI TÊN COLUMN 'id' THÀNH 'face_id'")
    print("="*50)
    
    # Xác nhận từ user
    confirm = input("Bạn có chắc chắn muốn đổi tên column 'id' thành 'face_id'? (y/n): ")
    
    if confirm.lower() in ['y', 'yes']:
        rename_column()
    else:
        print("❌ Đã hủy thao tác")