import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Ruta absoluta para que Render encuentre la carpeta templates siempre
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # La sintaxis (request=request) es la que pide la nueva versión
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/crm", response_class=HTMLResponse)
async def read_crm(request: Request):
    return templates.TemplateResponse(request=request, name="crm.html")

@app.get("/limpieza", response_class=HTMLResponse)
async def read_limpieza(request: Request):
    return templates.TemplateResponse(request=request, name="limpieza.html")

@app.get("/mantenimiento", response_class=HTMLResponse)
async def read_mantenimiento(request: Request):
    return templates.TemplateResponse(request=request, name="mantenimiento.html")

@app.get("/insumos", response_class=HTMLResponse)
async def read_insumos(request: Request):
    return templates.TemplateResponse(request=request, name="insumos.html")
