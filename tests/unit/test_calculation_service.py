import pytest
from app.services import CalculationService

class TestCalculationService:
    
    def test_add_operation(self):
        """Test addition operation"""
        result = CalculationService.perform_calculation("add", 5, 3)
        assert result == 8
    
    def test_subtract_operation(self):
        """Test subtraction operation"""
        result = CalculationService.perform_calculation("subtract", 10, 4)
        assert result == 6
    
    def test_multiply_operation(self):
        """Test multiplication operation"""
        result = CalculationService.perform_calculation("multiply", 6, 7)
        assert result == 42
    
    def test_divide_operation(self):
        """Test division operation"""
        result = CalculationService.perform_calculation("divide", 20, 4)
        assert result == 5
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            CalculationService.perform_calculation("divide", 10, 0)
    
    def test_invalid_operation(self):
        """Test invalid operation raises error"""
        with pytest.raises(ValueError, match="Invalid operation"):
            CalculationService.perform_calculation("power", 2, 3)
    
    def test_decimal_numbers(self):
        """Test calculation with decimal numbers"""
        result = CalculationService.perform_calculation("add", 1.5, 2.3)
        assert round(result, 1) == 3.8
    
    def test_negative_numbers(self):
        """Test calculation with negative numbers"""
        result = CalculationService.perform_calculation("multiply", -5, 3)
        assert result == -15
