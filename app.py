from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Esto detecta donde está parado el archivo y busca la carpeta templates ahí
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse("mantenimiento.html", {"request": request})

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse("insumos.html", {"request": request})
