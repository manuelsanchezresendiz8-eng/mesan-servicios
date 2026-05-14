from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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
# LEADS FILE
# =====================================================

LEADS_FILE = "leads.json"

if not os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, "w") as f:
        json.dump([], f)

# =====================================================
# HOME
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# =====================================================
# LIMPIEZA
# =====================================================

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})

# =====================================================
# MANTENIMIENTO
# =====================================================

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse("mantenimiento.html", {"request": request})

# =====================================================
# INSUMOS
# =====================================================

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse("insumos.html", {"request": request})

# =====================================================
# ADMIN (legacy)
# =====================================================

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)
    total_clientes = len(leads)
    total_cotizaciones = sum(lead.get("total_estimado", 0) for lead in leads)
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
# CRM
# =====================================================

@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)

    # Agregar índice a cada lead para poder actualizarlo
    for i, lead in enumerate(leads):
        lead["_id"] = i

    total_clientes = len(leads)
    total_cotizaciones = sum(lead.get("total_estimado", 0) for lead in leads)
    nuevos = sum(1 for l in leads if l.get("estado") == "nuevo")
    seguimiento = sum(1 for l in leads if l.get("estado") == "seguimiento")
    cerrados = sum(1 for l in leads if l.get("estado") == "cerrado")

    return templates.TemplateResponse(
        "crm.html",
        {
            "request": request,
            "clientes": total_clientes,
            "cotizaciones": round(total_cotizaciones, 2),
            "eficiencia": 94,
            "nuevos": nuevos,
            "seguimiento": seguimiento,
            "cerrados": cerrados,
            "leads": leads
        }
    )

# =====================================================
# API — GUARDAR LEAD
# =====================================================

@app.post("/leads")
async def guardar_lead(request: Request):
    try:
        data = await request.json()
        with open(LEADS_FILE, "r") as f:
            leads = json.load(f)

        nuevo_lead = {
            "nombre": data.get("nombre", "CLIENTE"),
            "servicio": data.get("servicio", "SERVICIO"),
            "total_estimado": float(data.get("total_estimado", 0)),
            "fecha": data.get("fecha", ""),
            "estado": data.get("estado", "nuevo"),
            "zona": data.get("zona", ""),
            "sector": data.get("sector", ""),
            "telefono": data.get("telefono", ""),
        }

        leads.append(nuevo_lead)

        with open(LEADS_FILE, "w") as f:
            json.dump(leads, f, indent=4)

        return {"ok": True}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# =====================================================
# API — ACTUALIZAR ESTADO LEAD
# =====================================================

@app.post("/leads/estado")
async def actualizar_estado(request: Request):
    try:
        data = await request.json()
        idx = int(data.get("id", -1))
        nuevo = data.get("estado", "nuevo")

        with open(LEADS_FILE, "r") as f:
            leads = json.load(f)

        if 0 <= idx < len(leads):
            leads[idx]["estado"] = nuevo
            with open(LEADS_FILE, "w") as f:
                json.dump(leads, f, indent=4)
            return {"ok": True}
        else:
            return {"ok": False, "error": "ID inválido"}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
async def health():
    return {"status": "ok"}
