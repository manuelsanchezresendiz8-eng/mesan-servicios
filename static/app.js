// static/app.js
async function captureGPS() {
    const status = document.getElementById("status");
    status.innerText = "Localizando dispositivo...";

    if (!navigator.geolocation) {
        status.innerText = "Error: Tu navegador no soporta GPS.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const coords = {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            };

            status.innerText = "Validando posición con MESAN Ω...";

            try {
                const response = await fetch("/api/checkin", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(coords)
                });

                const data = await response.json();

                if (data.resultado.valido) {
                    status.innerHTML = `<b style="color: #00f2ff;">CHECK-IN EXITOSO</b><br>Distancia: ${data.resultado.distancia}m`;
                } else {
                    status.innerHTML = `<b style="color: #ff4444;">FUERA DE RANGO</b><br>Estás a ${data.resultado.distancia}m del cliente.`;
                }

            } catch (error) {
                status.innerText = "Error de conexión con el servidor Ω.";
                console.error(error);
            }
        },
        (error) => {
            status.innerText = "Error: Por favor activa el GPS y permite el acceso.";
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}
