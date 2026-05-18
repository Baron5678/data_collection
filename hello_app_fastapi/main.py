from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .config import templates, BASE_DIR
from fastapi.staticfiles import StaticFiles

from hello_app_fastapi.routers import user_data

app = FastAPI(root_path="/fastapi")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

#Rendering home page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

app.include_router(user_data.router)
