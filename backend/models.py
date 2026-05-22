from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import JSONB # Dùng JSON cho SQLite nếu không xài Postgres
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# 1. Bảng Người dùng
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="student")

# 2. Bảng Tuần học (Week)
class Week(Base):
    __tablename__ = "weeks"
    
    week_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    order_num = Column(Integer, nullable=False)
    
    # Mối quan hệ: 1 Tuần có nhiều Bài tập
    exercises = relationship("Exercise", back_populates="week")

# 3. Bảng Bài tập (Exercise)
class Exercise(Base):
    __tablename__ = "exercises"
    
    exercise_id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("weeks.week_id"))
    title = Column(String(100), nullable=False)
    order_num = Column(Integer, nullable=False)
    
    week = relationship("Week", back_populates="exercises")
    activities = relationship("Activity", back_populates="exercise")

# 4. Bảng Hoạt động (Activity)
class Activity(Base):
    __tablename__ = "activities"
    
    activity_id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))
    activity_type = Column(String(50), nullable=False) # video, quiz, matching
    content = Column(JSONB, nullable=False) # Chứa câu hỏi & đáp án dạng JSON
    order_num = Column(Integer, nullable=False)
    
    exercise = relationship("Exercise", back_populates="activities")