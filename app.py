from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "MESAN OK"}

@app.get("/health")
def health():
    return {"status": "ok"}
