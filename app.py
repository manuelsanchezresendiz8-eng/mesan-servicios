from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Esto le dice a Python dónde están tus archivos HTML
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# RUTA 1: La Landing Page (Página principal)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# RUTA 2: El CRM (Control interno)
@app.get("/crm", response_class=HTMLResponse)
async def crm_page(request: Request):
    return templates.TemplateResponse("crm.html", {"request": request})

# RUTA 3: Limpieza (PDF)
@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza_page(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})
