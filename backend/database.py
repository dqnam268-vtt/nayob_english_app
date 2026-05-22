import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Lấy chuỗi kết nối từ biến môi trường (Environment Variable) nếu có
# Nếu không tìm thấy, hệ thống sẽ tự động dùng SQLite local như cũ để tránh lỗi
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./nayob_english.db"
)

# Khấu trừ lỗi tương thích chuỗi kết nối của SQLAlchemy đối với một số hosting
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Khởi tạo Engine tương ứng với loại Cơ sở dữ liệu
if DATABASE_URL.startswith("sqlite"):
    # Cấu hình riêng cho SQLite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Cấu hình tối ưu cho PostgreSQL Cloud (Neon/Supabase)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()