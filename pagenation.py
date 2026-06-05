# =============================================================
# STUDENT MANAGEMENT API v3.0 - Production-Quality
# Added: Input Validation, Pagination, Filtering, Error Handling
# =============================================================

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


# ----- Create the FastAPI application -----
app = FastAPI(
    title="Student Management API",
    description="Production-quality CRUD API with validation, pagination & filtering.",
    version="3.0.0"
)


# =============================================================
# DATA MODELS (Schemas) - Now with VALIDATION rules
# =============================================================

class StudentCreate(BaseModel):
    """
    Schema for creating a new student.
    Field() adds validation constraints.
    - min_length: minimum number of characters allowed
    - gt: greater than (age must be > 0)
    - lt: less than (age must be < 150)
    - pattern: a regex pattern the value must match
    """
    name: str = Field(
        ...,                    # ... means "this field is required"
        min_length=2,           # Name must be at least 2 characters
        max_length=100,         # Name cannot exceed 100 characters
        examples=["Kavinsuriya"]
    )
    age: int = Field(
        ...,
        gt=0,                   # Age must be greater than 0
        lt=150,                 # Age must be less than 150
        examples=[20]
    )
    grade: str = Field(
        ...,
        pattern=r"^[A-F][+-]?$",  # Only allows grades like A, B+, C-, D, F
        examples=["A"]
    )
    email: str = Field(
        ...,
        min_length=5,
        max_length=100,
        examples=["kavin@college.edu"]
    )

    # Custom validator: Check if email format is valid
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        # Simple regex to check email format: something@something.something
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format. Example: user@domain.com")
        return value


class StudentUpdate(BaseModel):
    """Schema for updating a student. All fields are optional."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, gt=0, lt=150)
    grade: Optional[str] = Field(None, pattern=r"^[A-F][+-]?$")
    email: Optional[str] = Field(None, min_length=5, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is not None:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, value):
                raise ValueError("Invalid email format. Example: user@domain.com")
        return value


# ----- In-memory database -----
students_db = []
next_id = 1


# =============================================================
# STANDARDIZED ERROR RESPONSE
# Instead of returning random error formats, we use a consistent
# structure so the client always knows what to expect.
# =============================================================
def error_response(status_code: int, message: str, details: str = None):
    """Create a standardized error response."""
    error = {
        "error": {
            "code": status_code,
            "message": message
        }
    }
    if details:
        error["error"]["details"] = details
    raise HTTPException(status_code=status_code, detail=error["error"])


# =============================================================
# ENDPOINT: Health Check
# =============================================================
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "total_students": len(students_db),
        "api_version": "3.0.0"
    }


# =============================================================
# ENDPOINT: CREATE a student (with validation)
# Now rejects invalid data automatically!
# =============================================================
@app.post("/api/v1/students", status_code=201)
def create_student(student: StudentCreate):
    global next_id

    # Check for duplicate email
    for existing in students_db:
        if existing["email"] == student.email:
            error_response(
                409,
                "Duplicate email",
                f"A student with email '{student.email}' already exists"
            )

    new_student = {
        "id": next_id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade,
        "email": student.email
    }

    students_db.append(new_student)
    next_id += 1

    return {
        "message": "Student created successfully",
        "student": new_student
    }


# =============================================================
# ENDPOINT: READ all students (with PAGINATION & FILTERING)
#
# Query Parameters:
#   ?page=1         → Which page of results (default: 1)
#   ?limit=10       → How many results per page (default: 10)
#   ?grade=A        → Filter by grade (optional)
#   ?search=kavin   → Search by name (optional)
#
# Example: GET /api/v1/students?page=1&limit=5&grade=A
# =============================================================
@app.get("/api/v1/students")
def get_all_students(
    page: int = Query(default=1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(default=10, ge=1, le=100, description="Results per page (max 100)"),
    grade: Optional[str] = Query(default=None, description="Filter by grade (e.g., A, B+)"),
    search: Optional[str] = Query(default=None, description="Search by student name")
):
    # Start with all students
    filtered = students_db.copy()

    # Apply grade filter if provided
    if grade:
        filtered = [s for s in filtered if s["grade"].lower() == grade.lower()]

    # Apply name search if provided
    if search:
        filtered = [s for s in filtered if search.lower() in s["name"].lower()]

    # Calculate pagination
    total_results = len(filtered)
    total_pages = max(1, (total_results + limit - 1) // limit)
    start_index = (page - 1) * limit
    end_index = start_index + limit

    # Slice the results for the requested page
    paginated = filtered[start_index:end_index]

    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": limit,
        "students": paginated
    }


# =============================================================
# ENDPOINT: READ a single student by ID
# =============================================================
@app.get("/api/v1/students/{student_id}")
def get_student(student_id: int):
    for student in students_db:
        if student["id"] == student_id:
            return {"student": student}

    error_response(404, "Student not found", f"No student exists with ID {student_id}")


# =============================================================
# ENDPOINT: UPDATE a student by ID (with validation)
# =============================================================
@app.put("/api/v1/students/{student_id}")
def update_student(student_id: int, updates: StudentUpdate):
    for student in students_db:
        if student["id"] == student_id:
            if updates.name is not None:
                student["name"] = updates.name
            if updates.age is not None:
                student["age"] = updates.age
            if updates.grade is not None:
                student["grade"] = updates.grade
            if updates.email is not None:
                # Check duplicate email for other students
                for other in students_db:
                    if other["id"] != student_id and other["email"] == updates.email:
                        error_response(
                            409,
                            "Duplicate email",
                            f"Email '{updates.email}' is already used by another student"
                        )
                student["email"] = updates.email

            return {
                "message": "Student updated successfully",
                "student": student
            }

    error_response(404, "Student not found", f"No student exists with ID {student_id}")


# =============================================================
# ENDPOINT: DELETE a student by ID
# =============================================================
@app.delete("/api/v1/students/{student_id}")
def delete_student(student_id: int):
    for i, student in enumerate(students_db):
        if student["id"] == student_id:
            deleted = students_db.pop(i)
            return {
                "message": "Student deleted successfully",
                "deleted_student": deleted
            }

    error_response(404, "Student not found", f"No student exists with ID {student_id}")
