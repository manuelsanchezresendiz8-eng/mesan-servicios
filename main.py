from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MESAN Servicios")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosCotizacion(BaseModel):
    empresa: str
    giro: str
    metros_cuadrados: float
    turnos: int
    criticidad: str
    correo: str
    telefono: str = "Sin definir"

@app.get("/")
def status():
    return {"status": "MESAN Servicios Operativo", "version": "v1.0"}

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
            "logistica": 1.05
        }
        factor_giro = factores_giro.get(data.giro.lower(), 1.0)
        factor_turnos = 1.0 + (data.turnos * 0.12)
        factor_criticidad = 1.25 if data.criticidad.lower() == "alta" else 1.0

        total = (data.metros_cuadrados * base_m2) * factor_giro * factor_turnos * factor_criticidad

        return {
            "folio": "MS-2026-001",
            "cliente": data.empresa,
            "propuesta_economica": round(total, 2),
            "moneda": "MXN",
            "mensaje": f"Cotizacion generada para {data.correo}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno")
