import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User

# Setup test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    """Create a test user and return credentials"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    return {"username": "testuser", "password": "testpass123"}

@pytest.fixture
def auth_token(test_user):
    """Get authentication token"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]

class TestAuthEndpoints:
    
    def test_register_success(self):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_duplicate_username(self, test_user):
        """Test registration with duplicate username"""
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "another@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self, test_user):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user["username"],
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

class TestCalculationEndpoints:
    
    def test_create_calculation(self, auth_token):
        """Test creating a calculation"""
        response = client.post(
            "/calculations/",
            json={
                "operation": "add",
                "operand1": 5,
                "operand2": 3
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "add"
    
    def test_create_calculation_unauthorized(self):
        """Test creating calculation without authentication"""
        response = client.post(
            "/calculations/",
            json={
                "operation": "add",
                "operand1": 5,
                "operand2": 3
            }
        )
        assert response.status_code == 401
    
    def test_create_calculation_divide_by_zero(self, auth_token):
        """Test division by zero validation"""
        response = client.post(
            "/calculations/",
            json={
                "operation": "divide",
                "operand1": 10,
                "operand2": 0
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 422
    
    def test_get_calculations(self, auth_token):
        """Test retrieving user's calculations"""
        # Create a calculation first
        client.post(
            "/calculations/",
            json={"operation": "add", "operand1": 5, "operand2": 3},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Get calculations
        response = client.get(
            "/calculations/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["result"] == 8

class TestHistoryEndpoints:
    
    def test_get_history(self, auth_token):
        """Test getting calculation history"""
        # Create some calculations
        for i in range(3):
            client.post(
                "/calculations/",
                json={"operation": "add", "operand1": i, "operand2": 1},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
        
        response = client.get(
            "/history/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 3
        assert len(data["calculations"]) == 3
    
    def test_get_statistics(self, auth_token):
        """Test getting calculation statistics"""
        # Create calculations
        client.post(
            "/calculations/",
            json={"operation": "add", "operand1": 10, "operand2": 5},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        client.post(
            "/calculations/",
            json={"operation": "multiply", "operand1": 3, "operand2": 4},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        response = client.get(
            "/history/statistics",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 2
        assert "operations_count" in data
        assert data["operations_count"]["add"] == 1
        assert data["operations_count"]["multiply"] == 1
    
    def test_clear_history(self, auth_token):
        """Test clearing calculation history"""
        # Create calculations
        client.post(
            "/calculations/",
            json={"operation": "add", "operand1": 5, "operand2": 3},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        # Clear history
        response = client.delete(
            "/history/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 204
        
        # Verify history is empty
        response = client.get(
            "/history/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        data = response.json()
        assert data["total_calculations"] == 0
