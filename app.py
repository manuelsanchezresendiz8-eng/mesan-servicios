import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Esto localiza tu carpeta de plantillas sin errores
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

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
