from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Đường dẫn kết nối CSDL (Hiện tại dùng SQLite cho tiện phát triển local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./nayob_english.db"
# Nếu chuyển sang PostgreSQL sau này, chuỗi sẽ có dạng:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Khởi tạo Engine xử lý kết nối
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Chỉ cần cho SQLite
)

# Khởi tạo Session để tương tác (Query, Insert, Update) với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Hàm Dependency dùng để mở và đóng kết nối tự động sau mỗi Request API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()