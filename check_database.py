#!/usr/bin/env python3
"""
Kiểm tra cấu trúc các table trong database
"""

import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

def check_tables():
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
            # Xem tất cả tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("📋 CÁC TABLE TRONG DATABASE:")
            for table in tables:
                print(f"  • {table[0]}")
            
            print("\n" + "="*50)
            
            # Kiểm tra cấu trúc table faces
            if ('faces',) in tables:
                print("📊 CẤU TRÚC TABLE 'faces':")
                cursor.execute("DESCRIBE faces;")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"  • {col[0]} ({col[1]})")
                
                # Đếm records
                cursor.execute("SELECT COUNT(*) FROM faces;")
                count = cursor.fetchone()[0]
                print(f"📈 Số records: {count}")
            
            print("\n" + "="*50)
            
            # Kiểm tra cấu trúc table face_embeddings (nếu có)
            if ('face_embeddings',) in tables:
                print("📊 CẤU TRÚC TABLE 'face_embeddings':")
                cursor.execute("DESCRIBE face_embeddings;")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"  • {col[0]} ({col[1]})")
                
                # Đếm records
                cursor.execute("SELECT COUNT(*) FROM face_embeddings;")
                count = cursor.fetchone()[0]
                print(f"📈 Số records: {count}")
            else:
                print("❌ TABLE 'face_embeddings' không tồn tại")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    print("🔍 KIỂM TRA CẤU TRÚC DATABASE")
    print("="*50)
    check_tables()