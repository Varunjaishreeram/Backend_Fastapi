from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes.student_routes import router as student_router

app = FastAPI()



@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

app.include_router(student_router)
