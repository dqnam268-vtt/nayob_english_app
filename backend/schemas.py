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

# ĐỊNH NGHĨA BỊ THIẾU: Dữ liệu nhận form tin nhắn (Feedback) từ học sinh
class FeedbackCreate(BaseModel):
    message: str
    location: str
    user_id: int