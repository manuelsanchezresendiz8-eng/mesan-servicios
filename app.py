from pydantic import BaseModel

# ----------------------------
# MODELOS
# ----------------------------

class DiagnosticoRequest(BaseModel):
    empresa: str
    sector: str
    problema: str


# ----------------------------
# DIAGNÓSTICO CEO (BASE)
# ----------------------------

@app.post("/diagnostico")
def diagnostico(data: DiagnosticoRequest):

    # simulación IA (luego lo conectamos a modelo real)
    return {
        "status": "ok",
        "empresa": data.empresa,
        "analisis": "Riesgo operativo detectado en supervisión y control de personal",
        "recomendacion": "Implementar MESAN Control para reducción de costos 20-40%",
        "upgrade": "Activar plan PRO"
    }
