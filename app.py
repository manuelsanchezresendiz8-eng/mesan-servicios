from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/crm")
def crm(request: Request):
    return templates.TemplateResponse(
        "crm.html",
        {"request": request}
    )


@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse(
        "limpieza.html",
        {"request": request}
    )


@app.get("/mantenimiento")
def mantenimiento(request: Request):
    return templates.TemplateResponse(
        "mantenimiento.html",
        {"request": request}
    )


@app.get("/insumos")
def insumos(request: Request):
    return templates.TemplateResponse(
        "insumos.html",
        {"request": request}
    )


@app.get("/health")
def health():
    return {"status": "ok"}
