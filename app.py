from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

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

@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    return templates.TemplateResponse(request=request, name="crm.html")
