from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Montar estáticos para CSS y JS
if os.path.exists(os.path.join(base_dir, "static")):
    app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Esta es tu Landing Page principal
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse(request=request, name="limpieza.html")

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse(request=request, name="mantenimiento.html")

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse(request=request, name="insumos.html")

# Si vas a meter el CRM, necesitamos una ruta para él
@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    return templates.TemplateResponse(request=request, name="crm.html")
