from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# ─────────────────────────────
# TEMPLATES
# ─────────────────────────────
templates = Jinja2Templates(directory="templates")

# ─────────────────────────────
# CRM EN MEMORIA (VERSIÓN 1)
# ─────────────────────────────
leads = []

class Lead(BaseModel):
    nombre: str
    servicio: str

# ─────────────────────────────
# LANDING PRINCIPAL
# ─────────────────────────────
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# ─────────────────────────────
# SERVICIO: LIMPIEZA
# ─────────────────────────────
@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )

# ─────────────────────────────
# SERVICIO: MANTENIMIENTO
# ─────────────────────────────
@app.get("/mantenimiento")
def mantenimiento(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mantenimiento.html"
    )

# ─────────────────────────────
# HEALTH CHECK
# ─────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}

# ─────────────────────────────
# CRM: CREAR LEAD
# ─────────────────────────────
@app.post("/lead")
def crear_lead(data: Lead):
    nuevo = {
        "nombre": data.nombre,
        "servicio": data.servicio,
        "fecha": datetime.now().isoformat()
    }
    leads.append(nuevo)

    return {
        "status": "ok",
        "lead": nuevo
    }

# ─────────────────────────────
# CRM: VER LEADS
# ─────────────────────────────
@app.get("/crm")
def ver_crm():
    return {
        "total": len(leads),
        "leads": leads
    }
