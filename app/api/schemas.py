from pydantic import BaseModel, Field
from app.domain.state import Direction

# Schema para a requisição de lançamento de uma sonda
class ProbeLaunchRequest(BaseModel):
    x: int = Field(..., ge=0, description="Coordenada X máxima da malha")
    y: int = Field(..., ge=0, description="Coordenada Y máxima da malha")
    direction: Direction # Pydantic valida automaticamente se o valor é um dos membros do Enum!

# Schema para a requisição de movimento da sonda
class ProbeMoveRequest(BaseModel):
    commands: str = Field(..., min_length=1, description="Sequência de comandos (L, R, M)")

# Schema padrão para a resposta de uma sonda
class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction

    class Config:
        # Permite que Pydantic leia os dados de um objeto (ex: nosso objeto Probe)
        from_attributes = True

# Schema para a resposta de listagem de todas as sondas
class AllProbesResponse(BaseModel):
    probes: list[ProbeResponse]