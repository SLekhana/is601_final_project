from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Calculation
from app.schemas import CalculationHistory, CalculationStatistics, CalculationResponse
from app.auth import get_current_user
from app.services import CalculationService

router = APIRouter(prefix="/history", tags=["History & Statistics"])

@router.get("/", response_model=CalculationHistory)
def get_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get calculation history for current user"""
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(Calculation.created_at.desc()).limit(limit).all()
    
    return {
        "total_calculations": len(calculations),
        "calculations": calculations
    }

@router.get("/statistics", response_model=CalculationStatistics)
def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for current user's calculations"""
    stats = CalculationService.get_user_statistics(db, current_user.id)
    return stats

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all calculation history for current user"""
    db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).delete()
    db.commit()
    return None
