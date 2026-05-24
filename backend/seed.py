# backend/seed.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Import cấu trúc bảng từ file models của bạn
import models

# 1. Kết nối tới Cơ sở dữ liệu đám mây qua biến môi trường
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./nayob_english.db" # Dự phòng nếu chạy ở máy cá nhân
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bộ mã hóa mật khẩu cho học sinh
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def run_seeder():
    db = SessionLocal()
    try:
        print("🔄 Đang kết nối và kiểm tra Cơ sở dữ liệu...")
        
        # Kiểm tra xem dữ liệu tuần đã tồn tại chưa để tránh ghi đè trùng lặp
        if db.query(models.Week).first():
            print("⚠️ Dữ liệu đã tồn tại trên đám mây, không cần chạy lại!")
            return

        print("🚀 Bắt đầu tiến trình bơm dữ liệu mẫu...")

        # --- TẠO TÀI KHOẢN HỌC SINH MẪU ---
        hashed_password = pwd_context.hash("123456")
        student = models.User(username="namy_student", password_hash=hashed_password, role="student")
        db.add(student)
        db.commit() # Lưu để lấy ID của học sinh

        # --- TẠO DỮ LIỆU TUẦN 1 (WEEK 1) ---
        w1 = models.Week(title="WEEK 1: PHONETICS & VOCABULARY", order_num=1)
        db.add(w1)
        db.commit()

        # Thêm Exercise 1 vào Tuần 1
        e1 = models.Exercise(title="EXERCISE 1", week_id=w1.week_id, order_num=1)
        db.add(e1)
        db.commit()

        # Thêm 3 Activity tương tác vào Exercise 1 (Dữ liệu lưu dạng JSON)
        a1 = models.Activity(
            exercise_id=e1.exercise_id, 
            activity_type="Video watching", 
            content={"url": "https://example.com/english-lesson1.mp4", "instruction": "Xem video và chú ý cách phát âm nguyên âm."}, 
            order_num=1
        )
        a2 = models.Activity(
            exercise_id=e1.exercise_id, 
            activity_type="Answering questions", 
            content={"question": "What is the main topic of the video?", "options": ["Grammar", "Pronunciation", "Vocabulary"], "correct": "Pronunciation"}, 
            order_num=2
        )
        a3 = models.Activity(
            exercise_id=e1.exercise_id, 
            activity_type="Matching meaning test", 
            content={"pairs": [{"word": "Acoustic", "meaning": "Thuộc về âm thanh"}, {"word": "Vowel", "meaning": "Nguyên âm"}]}, 
            order_num=3
        )
        db.add_all([a1, a2, a3])

        # Thêm Exercise 2 vào Tuần 1
        e2 = models.Exercise(title="EXERCISE 2", week_id=w1.week_id, order_num=2)
        db.add(e2)
        db.commit()


        # --- TẠO DỮ LIỆU TUẦN 2 (WEEK 2) ---
        w2 = models.Week(title="WEEK 2: GRAMMAR PRACTICE", order_num=2)
        db.add(w2)
        db.commit()
        
        e3 = models.Exercise(title="EXERCISE 1", week_id=w2.week_id, order_num=1)
        db.add(e3)

        # Lưu toàn bộ thay đổi vào PostgreSQL Online
        db.commit()
        print("🎉 Đã bơm toàn bộ cấu trúc bài học lên Cơ sở dữ liệu đám mây thành công!")

    except Exception as e:
        db.rollback()
        print(f"❌ Có lỗi xảy ra trong quá trình nạp dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeder()