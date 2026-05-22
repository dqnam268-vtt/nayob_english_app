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