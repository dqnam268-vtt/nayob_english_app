from pydantic import BaseModel

# Định nghĩa dữ liệu học sinh gửi lên khi đăng nhập
class UserLogin(BaseModel):
    username: str
    password: str

# Định nghĩa dữ liệu hệ thống trả về sau khi đăng nhập thành công
class LoginResponse(BaseModel):
    status: str
    message: str
    user_id: int
    role: str
    username: str

# Dữ liệu nhận form tin nhắn (Feedback) từ học sinh
class FeedbackCreate(BaseModel):
    message: str
    location: str
    user_id: int

# ==========================================
# THÊM MỚI: Định nghĩa dữ liệu khi tạo tài khoản
# ==========================================
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "student" # Mặc định tài khoản tạo ra là học sinh