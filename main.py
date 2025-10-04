from fastapi import FastAPI
from app.api.endpoints.probe_routes import router as probe_router
from app.database import engine
from app.repositories import database_models

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sonda em Marte API",
    description="API para controlar sondas de exploração em Marte.",
    version="1.0.0"
)

app.include_router(probe_router, prefix="/api", tags=["Probes"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API da Sonda em Marte! Acesse /docs para a documentação."}