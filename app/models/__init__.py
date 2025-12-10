from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import bcrypt

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    calculations = relationship("Calculation", back_populates="user", cascade="all, delete-orphan")
    
    def verify_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.hashed_password.encode('utf-8'))
    
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')


class Calculation(Base):
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation = Column(String, nullable=False)  # add, subtract, multiply, divide
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="calculations")
    
    def __repr__(self):
        return f"<Calculation {self.operation}: {self.operand1} and {self.operand2} = {self.result}>"
