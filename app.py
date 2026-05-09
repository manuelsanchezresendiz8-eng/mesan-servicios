from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Rutas corregidas para evitar el error de 'tuple'
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
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
