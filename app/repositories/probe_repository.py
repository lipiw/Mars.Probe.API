from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models import Probe

# --- O Contrato (Interface) ---

class IProbeRepository(ABC):
    """
    Define o contrato para um repositório de sondas.
    Qualquer implementação de repositório deve seguir esta interface.
    """
    @abstractmethod
    def save(self, probe: Probe) -> None:
        """Salva (cria ou atualiza) uma sonda."""
        pass

    @abstractmethod
    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        """Busca uma sonda pelo seu ID. Retorna None se não encontrar."""
        pass

    @abstractmethod
    def get_all(self) -> list[Probe]:
        """Retorna uma lista de todas as sondas."""
        pass

# --- A Implementação Concreta em Memória ---

class InMemoryProbeRepository(IProbeRepository):
    """
    Implementação do repositório que armazena as sondas em um
    dicionário em memória. Ideal para desenvolvimento e testes.
    """
    def __init__(self):
        # Nosso "banco de dados" em memória.
        # A chave será o ID da sonda, e o valor será o objeto Probe.
        self._probes: dict[str, Probe] = {}
        print("Repositório em memória inicializado.")

    def save(self, probe: Probe) -> None:
        """
        Salva a sonda no dicionário. Se o ID já existir,
        o objeto antigo será substituído pelo novo.
        """
        print(f"Salvando sonda com ID: {probe.id}")
        self._probes[probe.id] = probe

    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        """
        Busca a sonda no dicionário usando o método .get(),
        que retorna None por padrão se a chave não for encontrada.
        """
        print(f"Buscando sonda com ID: {probe_id}")
        return self._probes.get(probe_id)

    def get_all(self) -> list[Probe]:
        """Retorna uma lista com todos os objetos Probe armazenados."""
        print("Buscando todas as sondas...")
        return list(self._probes.values())