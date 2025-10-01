#!/usr/bin/env python3
"""
Script thêm cột 'description' vào table faces
"""

import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

def add_description_column():
    """Thêm cột description vào table faces"""
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
            print("🔄 Đang kiểm tra cấu trúc table 'faces'...")
            
            # Kiểm tra xem cột description đã tồn tại chưa
            cursor.execute("DESCRIBE faces;")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]
            
            print("📊 CÁC CỘT HIỆN TẠI:")
            for col in columns:
                print(f"  • {col[0]} ({col[1]})")
            
            if 'description' in column_names:
                print("✅ Cột 'description' đã tồn tại!")
                return
            
            print("\n🔄 Đang thêm cột 'description'...")
            
            # Thêm cột description
            sql = """
            ALTER TABLE faces 
            ADD COLUMN description TEXT NULL 
            COMMENT 'Mô tả thêm về người này'
            AFTER name
            """
            
            cursor.execute(sql)
            connection.commit()
            
            print("✅ Đã thêm cột 'description' thành công!")
            
            # Kiểm tra lại cấu trúc table
            print("\n📊 CẤU TRÚC TABLE 'faces' SAU KHI THÊM CỘT:")
            cursor.execute("DESCRIBE faces;")
            columns = cursor.fetchall()
            for col in columns:
                status = "🆕" if col[0] == 'description' else "  "
                print(f"{status} {col[0]} ({col[1]})")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    print("🔧 THÊM CỘT 'description' VÀO TABLE 'faces'")
    print("="*50)
    
    # Xác nhận từ user
    confirm = input("Bạn có chắc chắn muốn thêm cột 'description'? (y/n): ")
    
    if confirm.lower() in ['y', 'yes']:
        add_description_column()
    else:
        print("❌ Đã hủy thao tác")