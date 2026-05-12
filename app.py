from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# =========================
# LANDING PRINCIPAL
# =========================
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =========================
# LIMPIEZA
# =========================
@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )


# =========================
# MANTENIMIENTO
# =========================
@app.get("/mantenimiento")
def mantenimiento(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mantenimiento.html"
    )


# =========================
# CRM ADMIN
# =========================
@app.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "MESAN OK"}
