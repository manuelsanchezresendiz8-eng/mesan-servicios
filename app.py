from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import json
import os

# ============================================================
# APP
# ============================================================

app = FastAPI()

# ============================================================
# STATIC FILES
# ============================================================

app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(directory="templates")

# ============================================================
# MODELO LEAD
# ============================================================

class Lead(BaseModel):

    nombre: str
    servicio: str
    total_estimado: float
    estado: str = "nuevo"
    fecha: str

# ============================================================
# CREAR leads.json SI NO EXISTE
# ============================================================

if not os.path.exists("leads.json"):

    with open("leads.json", "w", encoding="utf-8") as f:
        json.dump([], f)

# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# ============================================================
# ADMIN CRM
# ============================================================

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):

    try:

        with open("leads.json", "r", encoding="utf-8") as f:
            leads = json.load(f)

    except:

        leads = []

    total_clientes = len(leads)

    total_cotizaciones = sum(
        float(l.get("total_estimado", 0))
        for l in leads
    )

    eficiencia = 85

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "clientes": total_clientes,
            "cotizaciones": round(total_cotizaciones, 2),
            "eficiencia": eficiencia,
            "leads": leads
        }
    )

# ============================================================
# API GUARDAR LEADS
# ============================================================

@app.post("/leads")
async def guardar_lead(lead: Lead):

    try:

        with open("leads.json", "r", encoding="utf-8") as f:
            leads = json.load(f)

    except:

        leads = []

    leads.append(lead.dict())

    with open("leads.json", "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=4, ensure_ascii=False)

    return JSONResponse({
        "status": "ok",
        "message": "Lead guardado"
    })

# ============================================================
# API OBTENER LEADS
# ============================================================

@app.get("/api/leads")
async def obtener_leads():

    try:

        with open("leads.json", "r", encoding="utf-8") as f:
            leads = json.load(f)

    except:

        leads = []

    return JSONResponse(leads)
