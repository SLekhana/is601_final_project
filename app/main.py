from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import init_db
from app.routers import auth, calculations, history

# Initialize FastAPI app
app = FastAPI(
    title="Calculator API",
    description="A calculator API with history and statistics tracking",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(calculations.router)
app.include_router(history.router)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Root endpoint - serve HTML page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
