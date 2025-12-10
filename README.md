# Calculator Application with History & Statistics

A full-stack calculator application built with FastAPI, featuring user authentication, calculation history tracking, and statistical analysis.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **BREAD Operations**: Browse, Read, Edit, Add, Delete calculations
- **Calculation History**: Track all your calculations with timestamps
- **Statistics Dashboard**: View usage statistics including:
  - Total calculations
  - Operations breakdown
  - Average values
  - Most used operation
- **RESTful API**: Complete API with OpenAPI documentation
- **Responsive UI**: Clean, modern interface
- **Docker Support**: Containerized application
- **CI/CD Pipeline**: Automated testing and deployment

## 📋 Prerequisites

- Python 3.11+
- Docker (optional)
- Git

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd is601_final_project
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the application**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the application**
- Web UI: http://localhost:8000

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# Unit tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# E2E tests (requires running server)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
pytest tests/e2e -v
```

### Test Coverage
```bash
pytest --cov=app --cov-report=html
```

## 📁 Project Structure
```
is601_final_project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database setup
│   ├── auth.py                 # Authentication logic
│   ├── models/
│   │   └── __init__.py         # SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py         # Pydantic schemas
│   ├── routers/
│   │   ├── auth.py             # Authentication routes
│   │   ├── calculations.py     # Calculation BREAD routes
│   │   └── history.py          # History & statistics routes
│   ├── services/
│   │   └── __init__.py         # Business logic
│   ├── templates/
│   │   ├── base.html           # Base template
│   │   └── index.html          # Main page
│   └── static/
│       ├── css/
│       │   └── style.css       # Styling
│       └── js/
│           ├── main.js         # Main JavaScript
│           └── calculator.js   # Calculator logic
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env
├── .gitignore
└── README.md
```

## 🔑 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token

### Calculations (BREAD)
- `POST /calculations/` - Create calculation (Add)
- `GET /calculations/` - Get all calculations (Browse)
- `GET /calculations/{id}` - Get specific calculation (Read)
- `DELETE /calculations/{id}` - Delete calculation (Delete)

### History & Statistics (NEW FEATURE)
- `GET /history/` - Get calculation history
- `GET /history/statistics` - Get usage statistics
- `DELETE /history/` - Clear all history

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT tokens with OAuth2
- **Password Hashing**: Bcrypt
- **Validation**: Pydantic v2

### Frontend
- **HTML Templates**: Jinja2
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS with Fetch API

### Testing
- **Unit Tests**: pytest
- **Integration Tests**: TestClient
- **E2E Tests**: Playwright

### DevOps
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Container Registry**: Docker Hub

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM
- CORS configuration
- Environment variable management

## 📊 Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- created_at

### Calculations Table
- id (Primary Key)
- user_id (Foreign Key)
- operation
- operand1
- operand2
- result
- created_at

## 🚢 Deployment

### Docker Hub

1. **Build image**
```bash
docker build -t yourusername/calculator-app:latest .
```

2. **Push to Docker Hub**
```bash
docker login
docker push yourusername/calculator-app:latest
```

3. **Pull and run**
```bash
docker pull yourusername/calculator-app:latest
docker run -p 8000:8000 yourusername/calculator-app:latest
```

### GitHub Actions

The CI/CD pipeline automatically:
1. Runs all tests on push/PR
2. Builds Docker image on successful tests
3. Pushes to Docker Hub on main/master branch

**Setup secrets in GitHub:**
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

## 📝 Environment Variables
```env
DATABASE_URL=sqlite:///./calculator.db
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🎯 Learning Outcomes Demonstrated

- ✅ CLO3: Python applications with automated testing
- ✅ CLO4: GitHub Actions for CI/CD
- ✅ CLO9: Docker containerization
- ✅ CLO10: REST API creation and testing
- ✅ CLO11: SQL database integration
- ✅ CLO12: JSON validation with Pydantic
- ✅ CLO13: Secure authentication implementation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Lekhana Sandra - IS 601 Final Project

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Playwright testing framework
- NJIT IS 601 Course
