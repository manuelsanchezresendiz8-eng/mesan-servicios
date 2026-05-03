from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import datetime

app = FastAPI(title="MESAN Servicios")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OMEGA_API = "https://mesan-api.onrender.com"

class DatosCotizacion(BaseModel):
    empresa: str
    giro: str
    m2: float
    turnos: int
    criticidad: str
    zona: str
    correo: str
    telefono: str = "Sin definir"
    nombre_contacto: str = ""

class PedidoInsumos(BaseModel):
    empresa: str
    telefono: str
    correo: str
    insumos: str
    urgencia: str = "normal"

@app.get("/")
def status():
    return {"status": "MESAN Servicios Operativo", "version": "v3.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/cotizar")
async def generar_cotizacion(data: DatosCotizacion):
    try:
        # 1. RENDIMIENTOS INDUSTRIALES (m2 por persona en 8h)
        rendimientos = {
            "alimenticio": 700,
            "metalmecanico": 1000,
            "logistica": 1500,
            "general": 1300
        }
        rendimiento_base = rendimientos.get(data.giro.lower(), 1000)

        # 2. PERSONAL REQUERIDO
        personal_por_turno = max(1, round(data.m2 / rendimiento_base))
        personal_total = personal_por_turno * data.turnos

        # 3. TARIFAS POR ZONA
        es_frontera = data.zona.lower() == "frontera"
        if es_frontera:
            costo_unidad_mensual = 19800
            iva = 0.08
            zona_label = "Zona Frontera"
        else:
            costo_unidad_mensual = 15500
            iva = 0.16
            zona_label = "Zona Interior"

        # 4. FACTOR CRITICIDAD
        factores = {"alta": 1.30, "media": 1.15, "baja": 1.0}
        factor_c = factores.get(data.criticidad.lower(), 1.0)

        # 5. CALCULO FINAL
        subtotal = (personal_total * costo_unidad_mensual) * factor_c
        total_propuesta = round(subtotal * (1 + iva), 2)
        precio_minimo = round(subtotal * (1 + iva) * 0.95, 2)
        precio_objetivo = round(subtotal * (1 + iva) * 1.10, 2)

        folio = f"MS-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(data.empresa) % 1000:03d}"

        # 6. GUARDAR LEAD EN MESAN OMEGA CRM
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    OMEGA_API + "/enterprise",
                    json={
                        "nombre": data.empresa,
                        "email": data.correo,
                        "telefono": data.telefono,
                        "giro": data.giro,
                        "contexto": (
                            f"Cotizacion MESAN Servicios | {zona_label} | "
                            f"{data.m2}m2 | {data.turnos} turno(s) | "
                            f"Criticidad: {data.criticidad} | "
                            f"Personal: {personal_total} | "
                            f"Propuesta: ${total_propuesta:,.2f} MXN/mes"
                        ),
                        "score": 75,
                        "clasificacion": "ALTO" if data.criticidad == "alta" else "MEDIO",
                        "impacto_min": int(total_propuesta),
                        "impacto_max": int(total_propuesta * 12)
                    }
                )
        except Exception:
            pass

        return {
            "folio": folio,
            "cliente": data.empresa,
            "zona": zona_label,
            "personal_requerido": personal_total,
            "elementos_por_turno": personal_por_turno,
            "propuesta": {
                "precio_minimo": precio_minimo,
                "precio_recomendado": total_propuesta,
                "precio_objetivo": precio_objetivo
            },
            "propuesta_economica": total_propuesta,
            "iva_aplicado": f"{int(iva*100)}%",
            "aviso_legal": "Estimacion basada en rendimientos estandar MESAN Servicios. Sujeta a levantamiento fisico."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insumos")
async def pedido_insumos(data: PedidoInsumos):
    try:
        cargo_entrega = 350 if data.urgencia == "urgente" else 150
        folio = f"INS-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(data.empresa) % 1000:03d}"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    OMEGA_API + "/enterprise",
                    json={
                        "nombre": data.empresa,
                        "email": data.correo,
                        "telefono": data.telefono,
                        "giro": "servicios",
                        "contexto": f"PEDIDO INSUMOS: {data.insumos}. Urgencia: {data.urgencia}. Cargo: ${cargo_entrega} MXN",
                        "score": 85,
                        "clasificacion": "ALTO",
                        "impacto_min": cargo_entrega,
                        "impacto_max": cargo_entrega * 12
                    }
                )
        except Exception:
            pass

        return {
            "ok": True,
            "folio": folio,
            "mensaje": f"Pedido recibido para {data.empresa}",
            "cargo_entrega": cargo_entrega,
            "urgencia": data.urgencia
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
