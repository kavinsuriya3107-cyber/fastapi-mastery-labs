from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# ── App setup ──────────────────────────────────────────
app = FastAPI(
    title="API Mastery Labs",
    description="Learning playground for building and attacking REST APIs.",
    version="1.0.0"
)

# ── In-memory storage ──────────────────────────────────
users_db = {}
user_id_counter = 1

# ── Pydantic models ────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "user"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

# ── Existing endpoints (don't remove) ──────────────────
@app.get("/")
def read_root():
    return {
        "message": "Welcome to your API Mastery Lab!",
        "status": "online",
        "phase": 4,
        "framework": "FastAPI"
    }

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "database": "in-memory"}

# ── CRUD endpoints ─────────────────────────────────────

# CREATE — add a new user
@app.post("/api/v1/users", status_code=201)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

# READ ALL — get every user
@app.get("/api/v1/users")
def get_all_users():
    return list(users_db.values())

# READ ONE — get a single user by ID
@app.get("/api/v1/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# UPDATE — change user details
@app.put("/api/v1/users/{user_id}")
def update_user(user_id: int, updates: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id]
    if updates.name is not None:
        user["name"] = updates.name
    if updates.email is not None:
        user["email"] = updates.email
    if updates.role is not None:
        user["role"] = updates.role
    return user

# DELETE — remove a user
@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = users_db.pop(user_id)
    return {"message": "User deleted", "user": deleted}