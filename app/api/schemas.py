from pydantic import BaseModel, Field
from app.domain.state import Direction

class ProbeLaunchRequest(BaseModel):
    x: int = Field(..., ge=0, description="Coordenada X máxima da malha")
    y: int = Field(..., ge=0, description="Coordenada Y máxima da malha")
    direction: Direction # Pydantic valida automaticamente se o valor é um dos membros do Enum

class ProbeMoveRequest(BaseModel):
    commands: str = Field(..., min_length=1, description="Sequência de comandos (L, R, M)")

class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction

    class Config:
        # Permite que Pydantic leia os dados de um objeto
        from_attributes = True

class AllProbesResponse(BaseModel):
    probes: list[ProbeResponse]