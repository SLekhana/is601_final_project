from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Calculation Schemas
class CalculationBase(BaseModel):
    operation: str = Field(..., pattern="^(add|subtract|multiply|divide)$")
    operand1: float
    operand2: float
    
    @validator('operand2')
    def check_division_by_zero(cls, v, values):
        if 'operation' in values and values['operation'] == 'divide' and v == 0:
            raise ValueError('Cannot divide by zero')
        return v

class CalculationCreate(CalculationBase):
    pass

class CalculationResponse(CalculationBase):
    id: int
    result: float
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

# History & Statistics Schemas
class CalculationHistory(BaseModel):
    total_calculations: int
    calculations: List[CalculationResponse]
    
class CalculationStatistics(BaseModel):
    total_calculations: int
    operations_count: dict
    average_operand1: Optional[float]
    average_operand2: Optional[float]
    average_result: Optional[float]
    most_used_operation: Optional[str]
    latest_calculation: Optional[CalculationResponse]
    
    class Config:
        from_attributes = True
