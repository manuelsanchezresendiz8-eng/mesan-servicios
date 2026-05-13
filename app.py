from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import json
import os

app = FastAPI()

# ─────────────────────────────
# TEMPLATES
# ─────────────────────────────
templates = Jinja2Templates(directory="templates")

# ─────────────────────────────
# STATIC FILES
# ─────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

# ─────────────────────────────
# VARIABLES MOTOR MESAN
# ─────────────────────────────
SMG = {
    "frontera": 440.62,
    "interior": 248.93
}

IVA = {
    "frontera": 0.08,
    "interior": 0.16
}

MARGEN = {
    "gobierno": 0.20,
    "industrial": 0.28,
    "corporativo": 0.35
}

# ─────────────────────────────
# HOME
# ─────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# ─────────────────────────────
# ADMIN CRM
# ─────────────────────────────
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):

    if not os.path.exists("leads.json"):
        leads = []
    else:
        with open("leads.json", "r", encoding="utf-8") as f:
            leads = json.load(f)

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

# ─────────────────────────────
# GUARDAR LEADS
# ─────────────────────────────
@app.post("/leads")
async def guardar_lead(request: Request):

    data = await request.json()

    if not os.path.exists("leads.json"):
        leads = []
    else:
        with open("leads.json", "r", encoding="utf-8") as f:
            leads = json.load(f)

    leads.append(data)

    with open("leads.json", "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=4, ensure_ascii=False)

    return JSONResponse({
        "status": "ok",
        "message": "Lead guardado correctamente"
    })

# ─────────────────────────────
# MOTOR COTIZADOR
# ─────────────────────────────
@app.post("/cotizar")
async def cotizar(request: Request):

    d = await request.json()

    zona = d.get("zona", "frontera")
    sector = d.get("sector", "corporativo")
    cantidad = int(d.get("cantidad", 1))
    turnos = int(d.get("turnos", 1))

    smg = SMG[zona]
    iva = IVA[zona]
    margen = MARGEN[sector]

    dias_mes = (6 / 7) * 30

    nomina = smg * dias_mes * turnos
    carga = nomina * 0.45

    insumos = 1200

    costo_total = (
        nomina +
        carga +
        insumos
    ) * cantidad

    subtotal = costo_total / (1 - margen)

    iva_total = subtotal * iva

    total = subtotal + iva_total

    return JSONResponse({
        "status": "ok",
        "total": round(total, 2),
        "subtotal": round(subtotal, 2),
        "iva": round(iva_total, 2)
    })
