# core/geocerca.py
import math

def verificar_presencia(lat_personal, lon_personal, lat_cliente, lon_cliente, radio=50):
    """
    Verifica si el trabajador está dentro del radio permitido (por defecto 50 metros).
    """
    radio_tierra = 6371000 # Radio de la Tierra en metros

    phi1 = math.radians(lat_personal)
    phi2 = math.radians(lat_cliente)

    delta_phi = math.radians(lat_cliente - lat_personal)
    delta_lambda = math.radians(lon_cliente - lon_personal)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = radio_tierra * c

    return {
        "valido": distancia <= radio,
        "distancia": round(distancia, 2)
    }
