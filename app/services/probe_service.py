from app.domain.models import Grid, Probe, InvalidMoveError
from app.domain.state import Direction
from app.repositories.probe_repository import IProbeRepository

class ProbeNotFoundError(Exception):
    pass

class InvalidCommandError(Exception):
    pass

class ProbeService:
    """
    Service de Probe, gerencia todas funcionalidade como o Repositorio, Grid, Probe
    """
    def __init__(self, probe_repository: IProbeRepository):
        self.repository = probe_repository

    def launch_probe(self, max_x: int, max_y: int, direction_str: str) -> Probe:
        try:
            initial_direction = Direction(direction_str.upper())
        except ValueError:
            raise InvalidCommandError(f"Direção inválida: '{direction_str}'. Use NORTH, EAST, SOUTH ou WEST.")

        grid = Grid(max_x=max_x, max_y=max_y)
        new_probe = Probe(grid=grid, initial_direction=initial_direction)

        self.repository.save(new_probe)
        return new_probe

    def move_probe(self, probe_id: str, commands: str) -> Probe:
        probe = self.repository.get_by_id(probe_id)
        if not probe:
            raise ProbeNotFoundError(f"Sonda com ID '{probe_id}' não encontrada.")

        valid_commands = {'L', 'R', 'M'}
        if not all(command in valid_commands for command in commands.upper()):
            raise InvalidCommandError("A sequência de comandos contém caracteres inválidos.")

        try:
            for command in commands.upper():
                if command == 'L':
                    probe.turn_left()
                elif command == 'R':
                    probe.turn_right()
                elif command == 'M':
                    probe.move()
        except InvalidMoveError as e:
            raise InvalidCommandError(f"A sequência de comandos '{commands}' resultou em um movimento inválido. Detalhes: {e}")

        self.repository.save(probe)
        return probe

    def get_all_probes(self) -> list[Probe]:
        return self.repository.get_all()