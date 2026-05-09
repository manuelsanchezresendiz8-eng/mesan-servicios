@app.get("/limpieza")
def limpieza(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="limpieza.html"
    )
