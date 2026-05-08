# routes/checkin.py
from flask import Blueprint, request, jsonify
from core.geocerca import verificar_presencia

checkin_bp = Blueprint("checkin", __name__)

# Coordenadas de prueba (CBTIS 21 Mexicali como referencia)
LAT_CLIENTE = 32.6322
LON_CLIENTE = -115.4411

@checkin_bp.route("/api/checkin", methods=["POST"])
def checkin():
    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")

    if lat is None or lon is None:
        return jsonify({
            "success": False,
            "message": "Coordenadas inválidas."
        }), 400

    # Llamamos al motor de geocerca que subiste antes
    resultado = verificar_presencia(
        lat,
        lon,
        LAT_CLIENTE,
        LON_CLIENTE
    )

    return jsonify({
        "success": True,
        "resultado": resultado,
        "sistema": "MESAN Ω"
    })
