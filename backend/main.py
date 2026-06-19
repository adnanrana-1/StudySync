import os
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="StudySync Application Engine Core")

# Locate directories dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Explicit error handling if directories are missing
if not os.path.exists(FRONTEND_DIR):
    print(f"CRITICAL DIRECTORY ERROR: Can't find 'frontend' folder at: {FRONTEND_DIR}")
    sys.exit(1)

# -------------------------------------------------------------
# PYDANTIC VALIDATION SCHEMAS
# -------------------------------------------------------------
class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    major: str = "Computer Science"

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# -------------------------------------------------------------
# REST API CONTROLLER ENDPOINTS
# -------------------------------------------------------------
@app.post("/api/auth/register", status_code=201)
async def register(payload: UserRegisterSchema):
    print(f"[REGISTRY SECURITY]: New account verified for: {payload.email}")
    return {"status": "success", "message": "Identity documentation recorded safely."}

@app.post("/api/auth/login")
async def login(payload: UserLoginSchema):
    print(f"[AUTH LAYER]: Evaluating login verification for: {payload.email}")
    return {
        "access_token": "secure_cryptographic_mock_token_sequence_xyz789",
        "token_type": "bearer",
        "username": "Adnan Ahmad Rana"
    }

# -------------------------------------------------------------
# CLEAN ROUTING PATHWAYS
# -------------------------------------------------------------
@app.get("/")
async def serve_login_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/register")
async def serve_register_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))

@app.get("/dashboard")
async def serve_dashboard_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

# This block must have ZERO indentation at the bottom of the file
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting StudySync Application Server...")
    print("👉 Access your app at: http://127.0.0.1:8001\n") # Updated port display
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info") # Changed 8000 to 8001