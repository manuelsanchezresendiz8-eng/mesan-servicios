from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import json
import os

# =====================================================
# APP Y SESIONES
# =====================================================

app = FastAPI()

SESSION_SECRET = os.environ.get("MESAN_SESSION_SECRET")
if not SESSION_SECRET:
    raise RuntimeError("Falta configurar MESAN_SESSION_SECRET")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=os.environ.get("MESAN_HTTPS_ONLY", "false").lower() == "true",
    max_age=8 * 60 * 60,
)

# Configure CRM_PASSWORD as an environment variable.
CRM_PASSWORD = os.environ.get("CRM_PASSWORD")
if not CRM_PASSWORD:
    raise RuntimeError("Falta configurar CRM_PASSWORD")
# =====================================================
# STATIC Y TEMPLATES
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")
LEADS_FILE = "leads.json"


# =====================================================
# UTILIDADES
# =====================================================

def crm_autenticado(request: Request) -> bool:
    return request.session.get("crm_authenticated") is True


def leer_leads():
    if not os.path.exists(LEADS_FILE):
        return []

    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if not isinstance(datos, list):
        raise ValueError("leads.json debe contener una lista")

    for i, lead in enumerate(datos):
        lead["_id"] = i

    return datos


def preparar_crm(request: Request):
    leads = leer_leads()

    total_clientes = len(leads)
    total_cotizaciones = sum(
        float(lead.get("total_estimado") or 0)
        for lead in leads
    )
    nuevos = sum(1 for lead in leads if lead.get("estado") == "nuevo")
    seguimiento = sum(
        1 for lead in leads if lead.get("estado") == "seguimiento"
    )
    cerrados = sum(
        1 for lead in leads if lead.get("estado") == "cerrado"
    )

    return {
        "request": request,
        "clientes": total_clientes,
        "cotizaciones": round(total_cotizaciones, 2),
        "eficiencia": 94,
        "nuevos": nuevos,
        "seguimiento": seguimiento,
        "cerrados": cerrados,
        "leads": leads,
    }


def guardar_leads(leads):
    # Elimina los identificadores temporales antes de guardar.
    datos = [
        {k: v for k, v in lead.items() if k != "_id"}
        for lead in leads
    ]

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# =====================================================
# HOME
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


# =====================================================
# LIMPIEZA
# =====================================================

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse(
        "limpieza.html", {"request": request}
    )


# =====================================================
# MANTENIMIENTO
# =====================================================

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse(
        "mantenimiento.html", {"request": request}
    )


# =====================================================
# INSUMOS
# =====================================================

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse(
        "insumos.html", {"request": request}
    )


# =====================================================
# PRIVACIDAD
# =====================================================

@app.get("/privacidad", response_class=HTMLResponse)
async def privacidad(request: Request):
    return templates.TemplateResponse(
        "privacidad.html", {"request": request}
    )


# =====================================================
# ADMIN LEGACY - REQUIERE SESION
# =====================================================

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    if not crm_autenticado(request):
        return RedirectResponse("/crm", status_code=303)

    return templates.TemplateResponse(
        "admin.html", preparar_crm(request)
    )


# =====================================================
# CRM - ACCESO Y PANEL
# =====================================================

@app.get("/crm", response_class=HTMLResponse)
async def crm_login(request: Request):
    if crm_autenticado(request):
        return templates.TemplateResponse(
            "crm.html", preparar_crm(request)
        )

    return templates.TemplateResponse(
        "crm_login.html",
        {"request": request, "error": ""},
    )


@app.post("/crm", response_class=HTMLResponse)
async def crm_access(request: Request, password: str = Form(...)):
    if password != CRM_PASSWORD:
        return templates.TemplateResponse(
            "crm_login.html",
            {
                "request": request,
                "error": "Contraseña incorrecta.",
            },
            status_code=401,
        )

    # Crea una sesión autenticada nueva.
    request.session.clear()
    request.session["crm_authenticated"] = True

    return templates.TemplateResponse(
        "crm.html", preparar_crm(request)
    )


@app.post("/crm/logout")
async def crm_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/crm", status_code=303)


# =====================================================
# API CRM - CONSULTA AUTENTICADA PARA ACTUALIZACION
# =====================================================

@app.get("/crm/data")
async def crm_data(request: Request):
    if not crm_autenticado(request):
        return JSONResponse(
            {"ok": False, "error": "No autenticado"},
            status_code=401,
        )

    try:
        contexto = preparar_crm(request)
        return {
            "ok": True,
            "clientes": contexto["clientes"],
            "cotizaciones": contexto["cotizaciones"],
            "eficiencia": contexto["eficiencia"],
            "nuevos": contexto["nuevos"],
            "seguimiento": contexto["seguimiento"],
            "cerrados": contexto["cerrados"],
            "leads": contexto["leads"],
        }
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "No se pudieron consultar los registros"},
            status_code=500,
        )


# =====================================================
# API - REGISTRO PUBLICO DE LEADS
# =====================================================

@app.post("/leads")
async def guardar_lead(request: Request):
    try:
        data = await request.json()

        if not isinstance(data, dict):
            return JSONResponse(
                {"ok": False, "error": "Datos inválidos"},
                status_code=400,
            )

        if data.get("origen") == "mantenimiento":
            for campo in ("nombre", "telefono", "servicio"):
                if not str(data.get(campo, "")).strip():
                    return JSONResponse(
                        {
                            "ok": False,
                            "error": f"Falta el campo obligatorio: {campo}",
                        },
                        status_code=400,
                    )

        nuevo_lead = {
            "nombre": str(data.get("nombre", "CLIENTE")).strip(),
            "servicio": str(data.get("servicio", "SERVICIO")).strip(),
            "total_estimado": float(data.get("total_estimado", 0)),
            "fecha": str(data.get("fecha", "")),
            # Los envios publicos siempre entran como nuevos.
            "estado": "nuevo",
            "zona": str(data.get("zona", "")),
            "sector": str(data.get("sector", "")),
            "empresa": str(data.get("empresa", "")),
            "telefono": str(data.get("telefono", "")),
            "correo": str(data.get("correo", "")),
            "rfc": str(data.get("rfc", "")),
            "cantidad": int(data.get("cantidad", 0)),
            "turnos": int(data.get("turnos", 1)),
            "con_insumos": bool(data.get("con_insumos", False)),
        }

        if data.get("origen") == "mantenimiento":
            nuevo_lead["tipo_registro"] = "solicitud_pendiente"

        leads = leer_leads()
        leads.append(nuevo_lead)
        guardar_leads(leads)

        return {"ok": True}

    except (ValueError, TypeError):
        return JSONResponse(
            {"ok": False, "error": "Formato de datos inválido"},
            status_code=400,
        )
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "No se pudo guardar la solicitud"},
            status_code=500,
        )


# =====================================================
# API - CAMBIO DE ESTADO AUTENTICADO
# =====================================================

@app.post("/leads/estado")
async def actualizar_estado(request: Request):
    if not crm_autenticado(request):
        return JSONResponse(
            {"ok": False, "error": "No autenticado"},
            status_code=401,
        )

    try:
        data = await request.json()
        idx = int(data.get("id", -1))
        nuevo = data.get("estado")

        if nuevo not in {"nuevo", "seguimiento", "cerrado"}:
            return JSONResponse(
                {"ok": False, "error": "Estado inválido"},
                status_code=400,
            )

        leads = leer_leads()

        if not 0 <= idx < len(leads):
            return JSONResponse(
                {"ok": False, "error": "ID inválido"},
                status_code=404,
            )

        leads[idx]["estado"] = nuevo
        guardar_leads(leads)

        return {"ok": True}

    except (ValueError, TypeError):
        return JSONResponse(
            {"ok": False, "error": "Solicitud inválida"},
            status_code=400,
        )
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "No se pudo actualizar el estado"},
            status_code=500,
        )


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
async def health():
    return {"status": "ok"}
