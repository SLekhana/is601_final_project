from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Calculation
from app.schemas import CalculationCreate, CalculationResponse
from app.auth import get_current_user
from app.services import CalculationService

router = APIRouter(prefix="/calculations", tags=["Calculations"])

@router.post("/", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calc_data: CalculationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new calculation"""
    try:
        # Perform the calculation
        result = CalculationService.perform_calculation(
            calc_data.operation,
            calc_data.operand1,
            calc_data.operand2
        )
        
        # Save to database
        db_calc = Calculation(
            user_id=current_user.id,
            operation=calc_data.operation,
            operand1=calc_data.operand1,
            operand2=calc_data.operand2,
            result=result
        )
        db.add(db_calc)
        db.commit()
        db.refresh(db_calc)
        return db_calc
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[CalculationResponse])
def get_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all calculations for current user"""
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return calculations

@router.get("/{calculation_id}", response_model=CalculationResponse)
def get_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific calculation"""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    
    return calculation

@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a calculation"""
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    
    db.delete(calculation)
    db.commit()
    return None
