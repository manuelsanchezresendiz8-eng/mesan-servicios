from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import uuid
from datetime import datetime

app = FastAPI(title="MESAN Servicios")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OMEGA_API = "https://mesan-api.onrender.com"
OMEGA_KEY = os.getenv("MESAN_API_KEY", "mesan2026mexicali")

class DatosCotizacion(BaseModel):
    empresa: str
    giro: str
    metros_cuadrados: float
    turnos: int
    criticidad: str
    correo: str
    telefono: str = "Sin definir"

class PedidoInsumos(BaseModel):
    empresa: str
    telefono: str
    correo: str
    insumos: str
    urgencia: str = "normal"

@app.get("/")
def status():
    return {"status": "MESAN Servicios Operativo", "version": "v2.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/cotizar")
async def calcular_propuesta(data: DatosCotizacion):
    try:
        base_m2 = 18.50
        factores_giro = {
            "alimenticio": 1.30,
            "metalmecanico": 1.15,
            "logistica": 1.05,
            "general": 1.0
        }
        factor_giro = factores_giro.get(data.giro.lower(), 1.0)
        factor_turnos = 1.0 + (data.turnos * 0.12)
        factor_criticidad = 1.25 if data.criticidad.lower() == "alta" else 1.05 if data.criticidad.lower() == "media" else 1.0

        total = (data.metros_cuadrados * base_m2) * factor_giro * factor_turnos * factor_criticidad

        # Guardar lead en MESAN Omega CRM
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    OMEGA_API + "/enterprise",
                    json={
                        "nombre": data.empresa,
                        "email": data.correo,
                        "telefono": data.telefono,
                        "giro": data.giro,
                        "contexto": f"Cotizacion MESAN Servicios: {data.metros_cuadrados}m2, {data.turnos} turnos, criticidad {data.criticidad}. Propuesta: ${round(total,2)} MXN/mes",
                        "score": 70,
                        "clasificacion": "MEDIO",
                        "impacto_min": int(total),
                        "impacto_max": int(total * 12)
                    }
                )
        except Exception:
            pass

        return {
            "folio": "MS-" + datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())[:4].upper(),
            "cliente": data.empresa,
            "propuesta_economica": round(total, 2),
            "moneda": "MXN",
            "mensaje": f"Cotizacion generada para {data.correo}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno")

@app.post("/insumos")
async def pedido_insumos(data: PedidoInsumos):
    try:
        cargo_entrega = 350 if data.urgencia == "urgente" else 150

        # Guardar lead en MESAN Omega CRM
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    OMEGA_API + "/enterprise",
                    json={
                        "nombre": data.empresa,
                        "email": data.correo,
                        "telefono": data.telefono,
                        "giro": "servicios",
                        "contexto": f"PEDIDO INSUMOS: {data.insumos}. Urgencia: {data.urgencia}. Cargo entrega: ${cargo_entrega} MXN",
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
            "mensaje": f"Pedido recibido para {data.empresa}",
            "cargo_entrega": cargo_entrega,
            "urgencia": data.urgencia,
            "folio": "INS-" + datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())[:4].upper()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno")
