from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Calculation
from typing import List, Dict, Optional

class CalculationService:
    @staticmethod
    def perform_calculation(operation: str, operand1: float, operand2: float) -> float:
        """Perform the calculation based on operation"""
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else None
        }
        
        if operation not in operations:
            raise ValueError(f"Invalid operation: {operation}")
        
        result = operations[operation](operand1, operand2)
        if result is None:
            raise ValueError("Cannot divide by zero")
        
        return result
    
    @staticmethod
    def get_user_statistics(db: Session, user_id: int) -> Dict:
        """Calculate statistics for a user's calculations"""
        calculations = db.query(Calculation).filter(
            Calculation.user_id == user_id
        ).all()
        
        if not calculations:
            return {
                "total_calculations": 0,
                "operations_count": {},
                "average_operand1": None,
                "average_operand2": None,
                "average_result": None,
                "most_used_operation": None,
                "latest_calculation": None
            }
        
        # Count operations
        operations_count = {}
        for calc in calculations:
            operations_count[calc.operation] = operations_count.get(calc.operation, 0) + 1
        
        # Calculate averages
        avg_operand1 = sum(c.operand1 for c in calculations) / len(calculations)
        avg_operand2 = sum(c.operand2 for c in calculations) / len(calculations)
        avg_result = sum(c.result for c in calculations) / len(calculations)
        
        # Most used operation
        most_used = max(operations_count.items(), key=lambda x: x[1])[0] if operations_count else None
        
        # Latest calculation
        latest = max(calculations, key=lambda x: x.created_at)
        
        return {
            "total_calculations": len(calculations),
            "operations_count": operations_count,
            "average_operand1": round(avg_operand1, 2),
            "average_operand2": round(avg_operand2, 2),
            "average_result": round(avg_result, 2),
            "most_used_operation": most_used,
            "latest_calculation": latest
        }
