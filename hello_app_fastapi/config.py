from fastapi.templating import Jinja2Templates
from pathlib import Path

# Templates configuration for rendering HTML pages in FastAPI
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
