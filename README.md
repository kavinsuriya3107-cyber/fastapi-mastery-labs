# 🚀 FastAPI Mastery Labs

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-202020?style=for-the-badge&logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io/)

Welcome to **FastAPI Mastery Labs**! This repository is a comprehensive learning playground demonstrating production-quality REST API design using Python and FastAPI, with a focus on input validation, pagination, filtering, and secure API architecture.

The project includes two distinct implementations:
- **`main.py`**: Basic CRUD API for user management (learning foundation)
- **`pagenation.py`**: Production-quality Student Management API v3.0 with advanced features

---

## 🛠️ Tech Stack & Tools

* **Language**: Python 3.10+
* **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
* **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
* **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
* **Testing**: `curl` & Swagger UI
* **Architecture**: REST API with in-memory database

---

## 🚀 Getting Started

Follow these steps to set up and run the API server locally on your machine.

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system:
```bash
python --version
```

### 2. Environment Setup
Create an isolated Python virtual environment to keep dependencies separate:

```bash
# Create the virtual environment
python -m venv venv
```

### 3. Activation
Activate the virtual environment depending on your OS:

* **Windows (PowerShell)**:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
* **macOS / Linux (Bash/Zsh)**:
  ```bash
  source venv/bin/activate
  ```

Once activated, your terminal prompt will display `(venv)`.

### 4. Install Dependencies
Install required packages from requirements.txt:
```bash
pip install -r requirements.txt
```

### 5. Running the API Servers

#### **Option A: Basic User Management API (main.py)**
```bash
uvicorn main:app --reload
```

#### **Option B: Advanced Student Management API (pagenation.py)**
```bash
uvicorn pagenation:app --reload
```

The server will start on `http://127.0.0.1:8000` with automatic reloading enabled.

---

## 📡 API Endpoints

### **Main API (main.py) - User Management**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Welcome message with API info |
| **GET** | `/api/v1/health` | Health check - returns server & database status |
| **POST** | `/api/v1/users` | Create new user |
| **GET** | `/api/v1/users` | Get all users |
| **GET** | `/api/v1/users/{user_id}` | Get single user by ID |
| **PUT** | `/api/v1/users/{user_id}` | Update user details |
| **DELETE** | `/api/v1/users/{user_id}` | Delete user by ID |

### **Advanced API (pagenation.py) - Student Management v3.0**

| Method | Endpoint | Description | Features |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/v1/health` | Health check | Returns total students count |
| **POST** | `/api/v1/students` | Create new student | ✅ Input validation, ✅ Email uniqueness |
| **GET** | `/api/v1/students` | Get all students | ✅ Pagination, ✅ Grade filter, ✅ Name search |
| **GET** | `/api/v1/students/{student_id}` | Get single student | Returns full student details |
| **PUT** | `/api/v1/students/{student_id}` | Update student | ✅ Validation, ✅ Duplicate email check |
| **DELETE** | `/api/v1/students/{student_id}` | Delete student | Removes from database |

#### **Pagination & Filtering Examples:**
```bash
# Get page 1 with 5 results per page
GET /api/v1/students?page=1&limit=5

# Filter by grade
GET /api/v1/students?grade=A

# Search by student name
GET /api/v1/students?search=kavin

# Combine filters: page 2, 10 results, grade A, search "kavin"
GET /api/v1/students?page=2&limit=10&grade=A&search=kavin
```

---

## ✨ Key Features

### **main.py - Foundation Level**
- ✅ Basic CRUD operations (Create, Read, Update, Delete)
- ✅ Simple error handling with HTTPException
- ✅ In-memory database (dictionary-based storage)
- ✅ Pydantic models for data validation
- ✅ Optional field updates
- ✅ User roles support (admin, user, etc.)

### **pagenation.py - Production Level**
- ✅ **Input Validation**: Field constraints (min/max length, regex patterns, value ranges)
- ✅ **Email Validation**: Custom regex validator with detailed error messages
- ✅ **Pagination**: Page-based results with configurable limit (1-100 items per page)
- ✅ **Filtering**: Filter students by grade (A, B+, C-, D, F, etc.)
- ✅ **Search**: Full-name substring search across all students
- ✅ **Error Handling**: Standardized error responses with meaningful messages
- ✅ **Duplicate Prevention**: Email uniqueness enforcement
- ✅ **Data Models**: Separate schemas for Create and Update operations
- ✅ **API Documentation**: Auto-generated Swagger UI with field descriptions

---

## 🎨 Interactive API Documentation (OpenAPI)

FastAPI automatically generates interactive API documentation:

* **Swagger UI**: `http://127.0.0.1:8000/docs` - Try endpoints with "Try it out" button
* **ReDoc**: `http://127.0.0.1:8000/redoc` - Clean, documentation-focused view
* **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json` - Raw OpenAPI specification

---

## 🔍 Request/Response Examples

### Create a Student (POST)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Kavin Suriya",
    "age": 20,
    "grade": "A",
    "email": "kavin@college.edu"
  }'
```

**Response:**
```json
{
  "message": "Student created successfully",
  "student": {
    "id": 1,
    "name": "Kavin Suriya",
    "age": 20,
    "grade": "A",
    "email": "kavin@college.edu"
  }
}
```

### Get Students with Pagination & Filtering
```bash
curl "http://127.0.0.1:8000/api/v1/students?page=1&limit=5&grade=A"
```

**Response:**
```json
{
  "total_results": 10,
  "total_pages": 2,
  "current_page": 1,
  "per_page": 5,
  "students": [
    {
      "id": 1,
      "name": "Kavin Suriya",
      "age": 20,
      "grade": "A",
      "email": "kavin@college.edu"
    }
  ]
}
```

### Create User (main.py)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
  }'
```

---

## 📚 Validation Rules (pagenation.py)

### Student Model Constraints:
- **Name**: 2-100 characters minimum and maximum
- **Age**: Must be between 1 and 149 years
- **Grade**: Pattern validation (A, A-, B+, B, B-, C+, C, C-, D, F)
- **Email**: Standard email format with custom regex pattern validation

### Error Responses:
- **400**: Invalid input data or validation failure
- **404**: Student/User not found
- **409**: Conflict (e.g., duplicate email address)
- **201**: Successful creation

---

## 🛡️ Security Best Practices Implemented

1. **Input Validation**: All user inputs are validated before processing
2. **Error Standardization**: Consistent error response format with meaningful messages
3. **Email Uniqueness**: Prevents duplicate email entries in database
4. **HTTP Status Codes**: Proper status codes (201 for creation, 404 for not found, 409 for conflict)
5. **Data Isolation**: Separate request/response schemas
6. **Type Safety**: Pydantic models enforce type correctness

---

## 🧪 Testing the API

### Health Check
```bash
curl http://127.0.0.1:8000/api/v1/health
```

### Get All Users (main.py)
```bash
curl http://127.0.0.1:8000/api/v1/users
```

### Get All Students with Pagination (pagenation.py)
```bash
curl "http://127.0.0.1:8000/api/v1/students?page=1&limit=10"
```

### Update User (main.py)
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "role": "user"}'
```

### Delete User
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/users/1"
```

---

## 📁 Project Structure

```
fastapi-mastery-labs/
├── main.py              # Basic CRUD API - User Management
├── pagenation.py        # Advanced API - Student Management v3.0
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

---

## 🚀 Learning Outcomes

By completing this lab, you'll understand:
- ✅ RESTful API design principles and best practices
- ✅ Input validation using Pydantic models
- ✅ Pagination and filtering implementation
- ✅ Error handling with standardized responses
- ✅ Database modeling with in-memory storage
- ✅ API documentation with OpenAPI/Swagger
- ✅ CRUD operations best practices
- ✅ HTTP status codes and REST semantics
- ✅ Custom validators for complex business logic
- ✅ Query parameter handling

---

## 📝 Requirements

```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

This is a learning project. Potential enhancements:
- Add database integration (SQLAlchemy, MongoDB)
- Implement authentication & authorization (JWT, OAuth2)
- Add comprehensive test suites (pytest)
- Deploy to cloud platforms (Heroku, AWS, GCP)
- Add rate limiting and caching
- Implement WebSocket support

---

## 📧 Contact & Support

Created by **Kavin Suriya** | GitHub: [@kavinsuriya3107-cyber](https://github.com/kavinsuriya3107-cyber)

For questions or discussions, please open an issue on this repository.

---

## 📜 License

This project is open source and available under the MIT License.

---

**Happy Learning! 🎓**