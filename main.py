from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# templates folder (your HTML files)
templates = Jinja2Templates(directory="templates")

# temporary storage (like database)
data_store = []

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data_store[::-1]   # latest first
    })

# ---------------- RECEIVE DATA FROM AI ----------------
@app.post("/violation")
def add_violation(data: dict):
    data_store.append(data)
    return {"status": "received"}

# ---------------- API CHECK ----------------
@app.get("/data")
def get_data():
    return data_store