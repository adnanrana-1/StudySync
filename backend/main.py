from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="StudySync Unified Live")

class UserRegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    major: str = "Computer Science"

class UserLoginSchema(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
async def register(payload: UserRegisterSchema):
    return {"status": "success", "message": "Registered successfully."}

@app.post("/api/auth/login")
async def login(payload: UserLoginSchema):
    return {
        "access_token": "mock_token_xyz123",
        "token_type": "bearer",
        "username": payload.email.split("@")[0].capitalize()
    }

@app.get("/", response_class=HTMLResponse)
async def serve_login():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>StudySync — Sign In</title><style>body { background: #0d1117; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }.box { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 40px; width: 350px; text-align: center; }input { width: 100%; padding: 10px; margin: 10px 0; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 4px; box-sizing: border-box; }button { width: 100%; padding: 12px; background: #4f46e5; border: none; color: #fff; font-weight: bold; border-radius: 4px; cursor: pointer; }a { color: #58a6ff; text-decoration: none; font-size: 14px; }</style></head><body><div class="box"><h2>Welcome to StudySync</h2><form id="f"><input type="email" id="e" placeholder="Email Address" required><input type="password" id="p" placeholder="Password" required><button type="submit">Sign In</button></form><p style="margin-top:15px;"><a href="/register">Create an account</a></p></div><script>document.getElementById("f").addEventListener("submit", async (e) => { e.preventDefault(); const res = await fetch("/api/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: document.getElementById("e").value, password: document.getElementById("p").value }) }); if (res.ok) { const data = await res.json(); localStorage.setItem("username", data.username); window.location.href = "/dashboard"; } else { alert("Login failed"); } });</script></body></html>"""

@app.get("/register", response_class=HTMLResponse)
async def serve_register():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>StudySync — Register</title><style>body { background: #0d1117; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }.box { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 40px; width: 350px; text-align: center; }input { width: 100%; padding: 10px; margin: 10px 0; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 4px; box-sizing: border-box; }button { width: 100%; padding: 12px; background: #4f46e5; border: none; color: #fff; font-weight: bold; border-radius: 4px; cursor: pointer; }a { color: #58a6ff; text-decoration: none; font-size: 14px; }</style></head><body><div class="box"><h2>Join Platform</h2><form id="f"><input type="text" id="n" placeholder="Full Name" required><input type="email" id="e" placeholder="Email Address" required><input type="password" id="p" placeholder="Password" required><button type="submit">Register Account</button></form><p style="margin-top:15px;"><a href="/">Already have an account? Sign In</a></p></div><script>document.getElementById("f").addEventListener("submit", async (e) => { e.preventDefault(); const res = await fetch("/api/auth/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: document.getElementById("n").value, email: document.getElementById("e").value, password: document.getElementById("p").value }) }); if (res.ok) { alert("Success!"); window.location.href = "/"; } });</script></body></html>"""

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>StudySync — Workspace</title><style>body { background: #12161a; color: #f0f2f5; font-family: sans-serif; display: flex; margin: 0; }.sidebar { width: 240px; background: #1a1f26; height: 100vh; padding: 30px 20px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; position: fixed; }.content { margin-left: 240px; padding: 40px; width: 100%; }.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }.card { background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }.btn-logout { background: none; border: 1px solid #f43f5e; color: #f43f5e; padding: 10px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }</style></head><body><div class="sidebar"><h2>🎓 StudySync</h2><button class="btn-logout" id="lo">Disconnect</button></div><div class="content"><h1 id="wel">Welcome Back!</h1><p>Your collaborative workspace is online and fully reactive.</p><div class="card-grid"><div class="card"><h3>Active Sessions</h3><h2>5</h2></div><div class="card" style="background: linear-gradient(135deg, #2b2212, #453315);"><h3>Peer Rating</h3><h2>4.9 ★</h2></div><div class="card" style="background: linear-gradient(135deg, #231c18, #3a2a22);"><h3>Study Hours</h3><h2>12.4h</h2></div></div></div><script>document.getElementById("wel").innerText = `Good Afternoon, ${localStorage.getItem("username") || "Scholar"}!`;document.getElementById("lo").addEventListener("click", () => { localStorage.clear(); window.location.href = "/"; });</script></body></html>"""