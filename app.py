from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import json
import os

# =====================================================
# APP
# =====================================================

app = FastAPI()

# =====================================================
# STATIC
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# =====================================================
# TEMPLATES
# =====================================================

templates = Jinja2Templates(directory="templates")

# =====================================================
# LEADS
# =====================================================

LEADS_FILE = "leads.json"

if not os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, "w") as f:
        json.dump([], f)

# =====================================================
# MODELO
# =====================================================

class Lead(BaseModel):
    nombre: str
    servicio: str
    total_estimado: float
    fecha: str
    estado: str

# =====================================================
# HOME
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# =====================================================
# LIMPIEZA
# =====================================================

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):

    return templates.TemplateResponse(
        "limpieza.html",
        {
            "request": request
        }
    )

# =====================================================
# MANTENIMIENTO
# =====================================================

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):

    return templates.TemplateResponse(
        "mantenimiento.html",
        {
            "request": request
        }
    )

# =====================================================
# INSUMOS
# =====================================================

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):

    return templates.TemplateResponse(
        "insumos.html",
        {
            "request": request
        }
    )

# =====================================================
# ADMIN CRM
# =====================================================

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):

    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)

    total_clientes = len(leads)

    total_cotizaciones = sum(
        lead.get("total_estimado", 0)
        for lead in leads
    )

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "clientes": total_clientes,
            "cotizaciones": round(total_cotizaciones, 2),
            "eficiencia": 94,
            "leads": leads
        }
    )

# =====================================================
# API LEADS
# =====================================================

@app.post("/leads")
async def guardar_lead(lead: Lead):

    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)

    leads.append(lead.dict())

    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=4)

    return {
        "ok": True
    }
