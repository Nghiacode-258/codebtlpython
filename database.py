import sqlite3

def connect():
    # Tạo và kết nối tới file CSDL tên là students_data.db
    return sqlite3.connect("students_data.db")

def init_db():
    conn = connect()
    cursor = conn.cursor()
    
    # Tạo bảng students với đầy đủ 8 cột. 
    # Cột 'id' sẽ tự động tăng và dùng làm khóa chính để Xóa/Sửa.
    # Đặt chữ [class] trong ngoặc vuông vì 'class' là từ khóa hệ thống của SQL.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mssv TEXT,
            name TEXT,
            [class] TEXT,
            major TEXT,
            birthday TEXT,
            phone TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()