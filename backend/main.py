from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas
from database import engine, get_db

# Tự động tạo các bảng trong Database dựa trên file models.py nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NamY English App API")

# Cấu hình CORS: Cho phép Frontend (chạy trên cổng khác hoặc file local) gọi được API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong thực tế nên giới hạn domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình mã hóa mật khẩu bằng thuật toán Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm tiện ích để kiểm tra mật khẩu
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ==========================================
# API TRANG CHỦ (Tránh lỗi Not Found)
# ==========================================
@app.get("/")
def read_root():
    return {"message": "Welcome to NamY English App API"}

# ==========================================
# API ĐĂNG NHẬP
# ==========================================
@app.post("/api/login", response_model=schemas.LoginResponse)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. Tìm kiếm người dùng trong DB bằng username
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    
    # 2. Nếu không tìm thấy user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác"
        )
        
    # 3. Kiểm tra mật khẩu (So sánh mật khẩu thô và mật khẩu đã băm trong DB)
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác"
        )
        
    # 4. Trả về thông tin đăng nhập thành công
    return {
        "status": "success",
        "message": "Đăng nhập thành công",
        "user_id": user.user_id,
        "role": user.role,
        "username": user.username
    }

# ==========================================
# API TẠO TÀI KHOẢN MỚI (DÀNH CHO ADMIN)
# ==========================================
@app.post("/api/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra xem tên đăng nhập này đã có ai dùng chưa
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Tên đăng nhập này đã tồn tại. Vui lòng chọn tên khác!"
        )
    
    # 2. Mã hóa mật khẩu an toàn
    hashed_password = pwd_context.hash(user.password)
    
    # 3. Tạo user mới và lưu vào Database
    new_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    
    return {"status": "success", "message": f"Đã tạo tài khoản '{user.username}' thành công!"}

# ==========================================
# CÁC API XỬ LÝ BÀI HỌC VÀ TƯƠNG TÁC
# ==========================================

# 1. API Lấy danh sách bài học (Đẩy ra Frontend)
@app.get("/api/get_syllabus")
def get_syllabus(db: Session = Depends(get_db)):
    # Truy vấn tất cả các Tuần, sắp xếp theo thứ tự
    weeks = db.query(models.Week).order_by(models.Week.order_num).all()
    
    result = []
    for week in weeks:
        week_data = {
            "week_id": week.week_id,
            "title": week.title,
            "exercises": []
        }
        for exc in week.exercises:
            # Lấy danh sách tên các hoạt động (Video, Quiz...) trong bài tập này
            activity_names = [act.activity_type for act in exc.activities]
            
            week_data["exercises"].append({
                "id": exc.exercise_id,
                "title": exc.title,
                "activities": activity_names
            })
        result.append(week_data)
        
    return result

# 2. API Nhận Feedback từ học sinh
@app.post("/api/send_feedback")
def receive_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(
        user_id=feedback.user_id,
        # Tạm ghép location vào message để hiển thị rõ ràng trên Streamlit Admin
        message=f"[{feedback.location}] {feedback.message}"
    )
    
    db.add(new_feedback)
    db.commit()
    return {"status": "success", "message": "Đã lưu phản hồi vào Database"}

# 3. API Tạo Dữ Liệu Mẫu (Chỉ chạy 1 lần)
@app.post("/api/seed_data")
def seed_data(db: Session = Depends(get_db)):
    # Kiểm tra xem đã có dữ liệu chưa để tránh tạo trùng lặp
    if db.query(models.Week).first():
        return {"message": "Dữ liệu đã tồn tại, không cần tạo lại!"}
    
    # Tạo 1 user mẫu (Lưu ý: Mật khẩu "123456" đã được mã hóa để đăng nhập được)
    hashed_pw = pwd_context.hash("123456")
    user = models.User(username="namy_student", password_hash=hashed_pw, role="student")
    db.add(user)
    db.commit()

    # Tạo Tuần 1
    w1 = models.Week(title="WEEK 1", order_num=1)
    db.add(w1)
    db.commit()

    # Tạo Bài tập 1 cho Tuần 1
    e1 = models.Exercise(title="EXERCISE 1", week_id=w1.week_id, order_num=1)
    db.add(e1)
    db.commit()

    # Tạo 3 Hoạt động cho Bài tập 1
    a1 = models.Activity(exercise_id=e1.exercise_id, activity_type="Video watching", content={"url": "video.mp4"}, order_num=1)
    a2 = models.Activity(exercise_id=e1.exercise_id, activity_type="Answering questions", content={"q1": "What is..."}, order_num=2)
    a3 = models.Activity(exercise_id=e1.exercise_id, activity_type="Matching meaning test", content={"pairs": []}, order_num=3)
    
    db.add_all([a1, a2, a3])
    db.commit()
    
    return {"message": "Đã bơm dữ liệu mẫu vào Database thành công!"}