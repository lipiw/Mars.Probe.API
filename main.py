from fastapi import FastAPI
from app.api.endpoints.probe_routes import router as probe_router

app = FastAPI(
    title="Sonda em Marte API",
    description="API para controlar sondas de exploração em Marte.",
    version="1.0.0"
)

# Inclui as rotas que definimos no nosso app principal
app.include_router(probe_router, prefix="/api", tags=["Probes"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API da Sonda em Marte! Acesse /docs para a documentação."}