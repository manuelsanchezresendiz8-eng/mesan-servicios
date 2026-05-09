from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.checkin import router as checkin_router
import uvicorn
import os

app = FastAPI(title="MESAN Ω Servicios")

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Registrar el router de checkin (el que ya tienes)
app.include_router(checkin_router)

# --- RUTAS DE NAVEGACIÓN Ω ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse("mantenimiento.html", {"request": request})

@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})

@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse("insumos.html", {"request": request})

if __name__ == "__main__":
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
