from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
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

# =============================================
# TARIFAS 2026
# =============================================
TARIFA_FRONTERA = 19800
TARIFA_INTERIOR  = 15500
IVA_FRONTERA     = 0.08
IVA_INTERIOR     = 0.16

# Factor de dificultad por tipo de area
FACTORES_AREA = {
    "oficinas":        1.0,
    "banos":           1.30,
    "almacen":         0.85,
    "produccion":      1.20,
    "comedor":         1.10,
    "estacionamiento": 0.70,
    "laboratorio":     1.50,
    "general":         1.0
}

# =============================================
# MODELOS
# =============================================
class DatosCotizacion(BaseModel):
    empresa: str
    correo: str
    telefono: str = "Sin definir"
    nombre_contacto: str = ""
    zona: str = "interior"
    elementos: int = 1
    areas: Dict[str, int] = {"general": 1}
    servicio: str = "limpieza"

class PedidoInsumos(BaseModel):
    empresa: str
    telefono: str
    correo: str
    insumos: str
    urgencia: str = "normal"

class PedidoDetallado(BaseModel):
    empresa: str
    telefono: str
    correo: str
    urgencia: str = "normal"
    multiuso: int = 0
    cloro: int = 0
    microfibras: int = 0
    jabon_polvo: int = 0
    aromatizante: int = 0
    pastillas_bano: int = 0

# =============================================
# CATALOGO INSUMOS
# =============================================
CATALOGO = {
    "multiuso":      {"nombre": "Limpiador Multiuso",    "unidad": "litro",       "precio_unitario": 45},
    "cloro":         {"nombre": "Cloro Industrial",      "unidad": "litro",       "precio_unitario": 28},
    "microfibras":   {"nombre": "Microfibras",           "unidad": "paquete x10", "precio_unitario": 120},
    "jabon_polvo":   {"nombre": "Jabon en Polvo",        "unidad": "kilo",        "precio_unitario": 35},
    "aromatizante":  {"nombre": "Aromatizante",          "unidad": "litro",       "precio_unitario": 55},
    "pastillas_bano":{"nombre": "Pastillas para Bano",   "unidad": "caja x12",   "precio_unitario": 85}
}

# =============================================
# ALGORITMO DE COTIZACION
# =============================================
def calcular_precio(elementos: int, areas: dict, zona: str):
    tarifa = TARIFA_FRONTERA if zona == "frontera" else TARIFA_INTERIOR
    iva    = IVA_FRONTERA    if zona == "frontera" else IVA_INTERIOR

    areas_activas = {k: v for k, v in areas.items() if v > 0}
    if not areas_activas:
        areas_activas = {"general": 1}

    total_areas = sum(areas_activas.values())
    factor = sum(
        FACTORES_AREA.get(k, 1.0) * v
        for k, v in areas_activas.items()
    ) / total_areas

    costo = elementos * tarifa * factor

    precio_minimo   = round(costo * 1.05 * (1 + iva), 2)
    precio_cierre   = round(costo * 1.15 * (1 + iva), 2)
    precio_ideal    = round(costo * 1.35 * (1 + iva), 2)
    margen          = round(((precio_cierre / (1 + iva) - costo) / (precio_cierre / (1 + iva))) * 100, 2)

    return {
        "costo_operativo": round(costo, 2),
        "precio_minimo":   precio_minimo,
        "precio_recomendado": precio_cierre,
        "precio_ideal":    precio_ideal,
        "margen":          margen,
        "iva":             f"{int(iva*100)}%",
        "zona_label":      "Zona Frontera" if zona == "frontera" else "Zona Interior"
    }

# =============================================
# ENDPOINTS
# =============================================
@app.get("/")
def status():
    return {"status": "MESAN Servicios Operativo", "version": "v4.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/catalogo")
def obtener_catalogo():
    return {"catalogo": CATALOGO}

@app.post("/cotizar")
async def cotizar(data: DatosCotizacion):
    try:
        precios = calcular_precio(data.elementos, data.areas, data.zona)
        folio = f"MS-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(data.empresa) % 1000:03d}"

        # Guardar lead en MESAN Omega CRM
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(
                    OMEGA_API + "/enterprise",
                    json={
                        "nombre": data.empresa,
                        "email": data.correo,
                        "telefono": data.telefono,
                        "giro": data.servicio,
                        "contexto": (
                            f"Cotizacion MESAN Servicios | {precios['zona_label']} | "
                            f"{data.elementos} elemento(s) | Areas: {data.areas} | "
                            f"Propuesta: ${precios['precio_recomendado']:,} MXN/mes"
                        ),
                        "score": 75,
                        "clasificacion": "ALTO",
                        "impacto_min": int(precios["precio_recomendado"]),
                        "impacto_max": int(precios["precio_recomendado"] * 12)
                    }
                )
        except Exception:
            pass

        return {
            "folio": folio,
            "cliente": data.empresa,
            "zona": precios["zona_label"],
            "elementos": data.elementos,
            "propuesta_economica": precios["precio_recomendado"],
            "iva_aplicado": precios["iva"],
            "aviso_legal": "Estimacion basada en tarifas MESAN Servicios 2026. Sujeta a levantamiento fisico.",
            # Internos — no mostrar al cliente
            "_interno": {
                "precio_minimo": precios["precio_minimo"],
                "precio_ideal":  precios["precio_ideal"],
                "margen":        precios["margen"],
                "costo_op":      precios["costo_operativo"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insumos")
async def pedido_insumos(data: PedidoInsumos):
    try:
        cargo = 350 if data.urgencia == "urgente" else 150
        folio = f"INS-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(data.empresa) % 1000:03d}"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(OMEGA_API + "/enterprise", json={
                    "nombre": data.empresa, "email": data.correo, "telefono": data.telefono,
                    "giro": "servicios",
                    "contexto": f"PEDIDO INSUMOS: {data.insumos}. Urgencia: {data.urgencia}. Cargo: ${cargo} MXN",
                    "score": 80, "clasificacion": "MEDIO",
                    "impacto_min": cargo, "impacto_max": cargo * 12
                })
        except Exception:
            pass
        return {"ok": True, "folio": folio, "cargo_entrega": cargo, "urgencia": data.urgencia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insumos/pedido")
async def pedido_detallado(data: PedidoDetallado):
    try:
        cargo = 350 if data.urgencia == "urgente" else 150
        folio = f"INS-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(data.empresa) % 1000:03d}"
        items = []
        subtotal = 0
        pedido_dict = data.dict()
        for producto, info in CATALOGO.items():
            cantidad = pedido_dict.get(producto, 0)
            if cantidad > 0:
                total_item = cantidad * info["precio_unitario"]
                subtotal += total_item
                items.append({"producto": info["nombre"], "cantidad": cantidad, "unidad": info["unidad"], "precio_unitario": info["precio_unitario"], "total": total_item})
        total_final = subtotal + cargo
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resumen = ", ".join([f"{i['producto']} x{i['cantidad']}" for i in items])
                await client.post(OMEGA_API + "/enterprise", json={
                    "nombre": data.empresa, "email": data.correo, "telefono": data.telefono,
                    "giro": "servicios",
                    "contexto": f"PEDIDO INSUMOS: {resumen}. Subtotal: ${subtotal}. Entrega: ${cargo}. Total: ${total_final} MXN",
                    "score": 80, "clasificacion": "MEDIO",
                    "impacto_min": total_final, "impacto_max": total_final * 12
                })
        except Exception:
            pass
        return {"ok": True, "folio": folio, "items": items, "subtotal": subtotal, "cargo_entrega": cargo, "total": total_final}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
