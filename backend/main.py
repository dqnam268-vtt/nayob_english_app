from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas
from database import engine, get_db

# Tự động tạo các bảng trong Database dựa trên file models.py nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NaYoB English App API")

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

# API Đăng nhập
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