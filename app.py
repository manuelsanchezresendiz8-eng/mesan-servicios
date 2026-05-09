from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def home():
    return FileResponse(os.path.join(BASE_DIR, "templates/index.html"))

@app.get("/crm")
async def crm():
    return FileResponse(os.path.join(BASE_DIR, "templates/crm.html"))

@app.get("/limpieza")
async def limpieza():
    return FileResponse(os.path.join(BASE_DIR, "templates/limpieza.html"))

@app.get("/mantenimiento")
async def mantenimiento():
    return FileResponse(os.path.join(BASE_DIR, "templates/mantenimiento.html"))

@app.get("/insumos")
async def insumos():
    return FileResponse(os.path.join(BASE_DIR, "templates/insumos.html"))
