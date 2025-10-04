import uuid
from dataclasses import dataclass, field

from app.domain.state import IDirectionState, DIRECTION_STATE_MAP, Direction

class InvalidMoveError(Exception):
    pass


# Value Object
@dataclass(frozen=True)
class Position:
    """Posição da Sonda."""
    x: int
    y: int


@dataclass
class Grid:
    """Classe responsavel pela Malha, onde a Sonda ira se mover."""
    max_x: int
    max_y: int

    def is_valid_position(self, position: Position) -> bool:
        is_valid_x = 0 <= position.x <= self.max_x
        is_valid_y = 0 <= position.y <= self.max_y
        return is_valid_x and is_valid_y


class Probe:
    """Classe sobre a Sonda em si, contem todos metodos para o gerenciamento de uma Sonda."""
    def __init__(self, grid: Grid, initial_direction: Direction, probe_id: str = None, initial_position: Position = Position(0, 0)):

        if not grid.is_valid_position(initial_position):
            raise InvalidMoveError(f"A posição inicial {initial_position} está fora da malha.")

        self.id: str = probe_id or str(uuid.uuid4())
        self.position: Position = initial_position
        self.direction_state: IDirectionState = DIRECTION_STATE_MAP[initial_direction]
        self.grid: Grid = grid

    @property
    def current_direction(self) -> Direction:
        return self.direction_state.direction

    def turn_left(self):
        self.direction_state = self.direction_state.turn_left()
        print(f"Sonda {self.id} virou para a esquerda. Nova direção: {self.current_direction.value}")

    def turn_right(self):
        self.direction_state = self.direction_state.turn_right()
        print(f"Sonda {self.id} virou para a direita. Nova direção: {self.current_direction.value}")

    def move(self):
        next_x, next_y = self.direction_state.move(self.position.x, self.position.y)
        next_position = Position(x=next_x, y=next_y)

        if not self.grid.is_valid_position(next_position):
            raise InvalidMoveError(f"Movimento para {next_position} é inválido e ultrapassa os limites da malha.")

        self.position = next_position
        print(f"Sonda {self.id} moveu-se para {self.position}. Direção: {self.current_direction.value}")