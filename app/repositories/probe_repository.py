from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models import Probe

class IProbeRepository(ABC):
    """Interface para o armazenamento e gerenciamento de sondas."""
    @abstractmethod
    def save(self, probe: Probe) -> None:
        pass

    @abstractmethod
    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        pass

    @abstractmethod
    def get_all(self) -> list[Probe]:
        pass


class InMemoryProbeRepository(IProbeRepository):
    """
    Implementação do repositório que armazena as sondas em um
    dicionário em memória.
    """
    def __init__(self):
        self._probes: dict[str, Probe] = {}
        print("Repositório em memória inicializado.")

    def save(self, probe: Probe) -> None:
        print(f"Salvando sonda com ID: {probe.id}")
        self._probes[probe.id] = probe

    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        print(f"Buscando sonda com ID: {probe_id}")
        return self._probes.get(probe_id)

    def get_all(self) -> list[Probe]:
        print("Buscando todas as sondas...")
        return list(self._probes.values())