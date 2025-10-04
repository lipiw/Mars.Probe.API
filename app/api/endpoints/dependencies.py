from app.services.probe_service import ProbeService
from app.repositories.sqlalchemy_probe_repository import SQLAlchemyProbeRepository
from app.database import SessionLocal

probe_repo = SQLAlchemyProbeRepository(db_session_factory=SessionLocal)

def get_probe_service() -> ProbeService:
    """
    Função de dependência que cria e retorna uma instância de ProbeService, injetando o repositório singleton.
    """
    return ProbeService(probe_repository=probe_repo)