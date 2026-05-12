from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from reportlab.pdfgen import canvas
import json

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

    with open("leads.json", "r") as file:
        leads = json.load(file)

    leads.append(resultado)

    with open("leads.json", "w") as file:
        json.dump(leads, file, indent=4)

    pdf_name = f"cotizacion_{telefono}.pdf"

    c = canvas.Canvas(pdf_name)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "MESAN Servicios")

    c.setFont("Helvetica", 12)

    c.drawString(50, 760, f"Cliente: {nombre}")
    c.drawString(50, 740, f"Empresa: {empresa}")
    c.drawString(50, 720, f"Ciudad: {ciudad}")
    c.drawString(50, 700, f"Servicio: {servicio}")
    c.drawString(50, 680, f"Inmueble: {inmueble}")
    c.drawString(50, 660, f"Metros cuadrados: {metros}")
    c.drawString(50, 640, f"Frecuencia: {frecuencia}")

    c.setFont("Helvetica-Bold", 16)

    c.drawString(
        50,
        590,
        f"Total estimado: ${round(total,2)} MXN"
    )

    c.setFont("Helvetica", 11)

    c.drawString(
        50,
        540,
        "Cotización generada automáticamente por MESAN Servicios."
    )

    c.save()

    return FileResponse(
        pdf_name,
        media_type="application/pdf",
        filename=pdf_name
    )


@app.get("/health")
async def health():
    return {"status": "MESAN OK"}
