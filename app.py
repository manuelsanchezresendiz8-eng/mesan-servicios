from fastapi import FastAPI, Request
from fastapi.responses import HTML_Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.checkin import router as checkin_router
import uvicorn

app = FastAPI(title="MESAN Ω Servicios")

# Montar archivos estáticos y plantillas
# Importante: Asegúrate de que las carpetas 'static' y 'templates' existan en la raíz
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Registrar el router de checkin
app.include_router(checkin_router)

@app.get("/", response_class=HTML_Response)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
