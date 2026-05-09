from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )


@app.get("/mantenimiento")
def mantenimiento(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mantenimiento.html"
    )


@app.get("/health")
def health():
    return {"status": "ok"}
