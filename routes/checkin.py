from fastapi import APIRouter
from pydantic import BaseModel
from core.geocerca import verificar_presencia # Esto busca dentro de la carpeta core

router = APIRouter()

class Coords(BaseModel):
    lat: float
    lon: float

# Coordenadas de prueba en Mexicali
LAT_CLIENTE = 32.6322
LON_CLIENTE = -115.4411

@router.post("/api/checkin")
async def checkin(coords: Coords):
    resultado = verificar_presencia(coords.lat, coords.lon, LAT_CLIENTE, LON_CLIENTE)
    return {"success": True, "resultado": resultado, "sistema": "MESAN Ω (FastAPI)"}
