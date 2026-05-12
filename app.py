from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/limpieza", response_class=HTMLResponse)
async def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )


@app.get("/mantenimiento", response_class=HTMLResponse)
async def mantenimiento(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mantenimiento.html"
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )


@app.get("/crm", response_class=HTMLResponse)
async def crm(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="crm.html"
    )


@app.get("/insumos", response_class=HTMLResponse)
async def insumos(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="insumos.html"
    )


@app.get("/health")
async def health():
    return {"status": "MESAN OK"}
