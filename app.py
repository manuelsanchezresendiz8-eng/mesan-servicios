from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )


@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mantenimiento.html"
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )


@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="crm.html"
    )


@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="insumos.html"
    )


@app.post("/cotizar")
async def cotizar(
    nombre: str = Form(...),
    empresa: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    ciudad: str = Form(...),
    inmueble: str = Form(...),
    metros: int = Form(...),
    frecuencia: str = Form(...),
    servicio: str = Form(...),
    horario: str = Form(...),
    comentarios: str = Form("")
):

    # MOTOR FINANCIERO BASE MESAN

    base_m2 = 12

    if servicio == "Limpieza profunda":
        base_m2 = 16

    elif servicio == "Limpieza hospitalaria":
        base_m2 = 22

    elif servicio == "Limpieza industrial":
        base_m2 = 28

    subtotal = metros * base_m2

    if frecuencia == "Diario":
        subtotal *= 1.4

    elif frecuencia == "3 veces por semana":
        subtotal *= 1.2

    iva = subtotal * 0.16

    total = subtotal + iva

    resultado = {
        "cliente": nombre,
        "empresa": empresa,
        "telefono": telefono,
        "correo": correo,
        "ciudad": ciudad,
        "inmueble": inmueble,
        "metros": metros,
        "frecuencia": frecuencia,
        "servicio": servicio,
        "horario": horario,
        "comentarios": comentarios,
        "total_estimado": round(total, 2),
        "estatus": "Cotización generada"
    }

    print(resultado)

    return JSONResponse(content=resultado)


@app.get("/health")
async def health():
    return {"status": "MESAN OK"}
