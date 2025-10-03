from app.repositories.probe_repository import InMemoryProbeRepository
from app.services.probe_service import ProbeService

# Criamos uma única instância do repositório (nosso "banco de dados" em memória)
# Esta instância será compartilhada por toda a aplicação durante sua execução.
probe_repo = InMemoryProbeRepository()

def get_probe_service() -> ProbeService:
    """
    Função de dependência que cria e retorna uma instância de ProbeService,
    injetando o repositório singleton.
    """
    return ProbeService(probe_repository=probe_repo)