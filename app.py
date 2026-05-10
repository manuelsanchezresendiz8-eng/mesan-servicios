from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ─────────────────────────────
# BASE DE DATOS LOCAL (PERSISTENTE)
# ─────────────────────────────
conn = sqlite3.connect("mesan.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    servicio TEXT,
    fecha TEXT
)
""")
conn.commit()

# ─────────────────────────────
# MODELO
# ─────────────────────────────
class Lead(BaseModel):
    nombre: str
    servicio: str

# ─────────────────────────────
# LANDING
# ─────────────────────────────
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse("limpieza.html", {"request": request})

@app.get("/mantenimiento")
def mantenimiento(request: Request):
    return templates.TemplateResponse("mantenimiento.html", {"request": request})

# ─────────────────────────────
# HEALTH
# ─────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}

# ─────────────────────────────
# CREAR LEAD (PERSISTENTE)
# ─────────────────────────────
@app.post("/lead")
def crear_lead(data: Lead):
    cursor.execute(
        "INSERT INTO leads (nombre, servicio, fecha) VALUES (?, ?, ?)",
        (data.nombre, data.servicio, datetime.now().isoformat())
    )
    conn.commit()

    return {"status": "ok"}

# ─────────────────────────────
# VER CRM
# ─────────────────────────────
@app.get("/crm")
def ver_crm():
    cursor.execute("SELECT * FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()

    leads = [
        {"id": r[0], "nombre": r[1], "servicio": r[2], "fecha": r[3]}
        for r in rows
    ]

    return {
        "total": len(leads),
        "leads": leads
    }
