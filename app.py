import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configuración de rutas absoluta para Render
base_dir = os.path.dirname(os.path.realpath(__file__))
templates_path = os.path.join(base_dir, "templates")
templates = Jinja2Templates(directory=templates_path)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/crm", response_class=HTMLResponse)
async def read_crm(request: Request):
    return templates.TemplateResponse("crm.html", {"request": request})

@app.get("/limpieza", response_class=HTMLResponse)
async def read_limpieza(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})

@app.get("/mantenimiento", response_class=HTMLResponse)
async def read_mantenimiento(request: Request):
    return templates.TemplateResponse("mantenimiento.html", {"request": request})

@app.get("/insumos", response_class=HTMLResponse)
async def read_insumos(request: Request):
    return templates.TemplateResponse("insumos.html", {"request": request})
