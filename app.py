from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# LANDING PRINCIPAL
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# CRM
@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    return templates.TemplateResponse(
        "crm.html",
        {"request": request}
    )

# LIMPIEZA
@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse(
        "limpieza.html",
        {"request": request}
    )

# MANTENIMIENTO
@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse(
        "mantenimiento.html",
        {"request": request}
    )

# INSUMOS
@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse(
        "insumos.html",
        {"request": request}
    )
