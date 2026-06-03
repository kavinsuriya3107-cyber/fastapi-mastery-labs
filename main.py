from fastapi import FastAPI

app = FastAPI(
    title="API Mastery Labs",
    description="Your learning playground for building secure REST APIs with Python & FastAPI.",
    version="1.0.0"
)

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
    return {"status": "healthy", "database": "disconnected"}
