from app.domain.models import Grid, Probe, InvalidMoveError
from app.domain.state import Direction
from app.repositories.probe_repository import IProbeRepository

class ProbeNotFoundError(Exception):
    pass

class InvalidCommandError(Exception):
    pass

class ProbeService:
    def __init__(self, probe_repository: IProbeRepository):
        """
        O serviço recebe uma implementação de IProbeRepository.
        Isso é a Injeção de Dependência.
        """
        self.repository = probe_repository

    def launch_probe(self, max_x: int, max_y: int, direction_str: str) -> Probe:
        """
        Caso de uso: Lançar uma nova sonda.
        Coordena a criação dos objetos de domínio e os salva no repositório.
        """
        try:
            # O serviço traduz dados "primitivos" (str) para objetos de domínio (Enum)
            initial_direction = Direction(direction_str.upper())
        except ValueError:
            raise InvalidCommandError(f"Direção inválida: '{direction_str}'. Use NORTH, EAST, SOUTH ou WEST.")

        grid = Grid(max_x=max_x, max_y=max_y)
        new_probe = Probe(grid=grid, initial_direction=initial_direction)

        self.repository.save(new_probe)
        return new_probe

    def move_probe(self, probe_id: str, commands: str) -> Probe:
        """
        Caso de uso: Mover uma sonda com uma sequência de comandos.
        """
        probe = self.repository.get_by_id(probe_id)
        if not probe:
            raise ProbeNotFoundError(f"Sonda com ID '{probe_id}' não encontrada.")

        # Validação dos comandos antes de começar a execução
        valid_commands = {'L', 'R', 'M'}
        if not all(command in valid_commands for command in commands.upper()):
            raise InvalidCommandError("A sequência de comandos contém caracteres inválidos.")

        # Executa os comandos na instância da sonda
        try:
            for command in commands.upper():
                if command == 'L':
                    probe.turn_left()
                elif command == 'R':
                    probe.turn_right()
                elif command == 'M':
                    probe.move()
        except InvalidMoveError as e:
            # Se um movimento inválido ocorrer, a exceção do domínio é capturada
            # e nós a relançamos como um erro de comando inválido,
            # preservando a mensagem original.
            raise InvalidCommandError(f"A sequência de comandos '{commands}' resultou em um movimento inválido. Detalhes: {e}")

        # Se todos os comandos foram executados com sucesso, salvamos o estado final.
        self.repository.save(probe)
        return probe

    def get_all_probes(self) -> list[Probe]:
        """
        Caso de uso: Obter todas as sondas.
        Simplesmente delega a chamada para o repositório.
        """
        return self.repository.get_all()