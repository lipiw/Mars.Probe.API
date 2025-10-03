import uuid
from dataclasses import dataclass, field

from app.domain.state import IDirectionState, DIRECTION_STATE_MAP, Direction

class InvalidMoveError(Exception):
    pass


# Position é um "Value Object": um objeto definido por seus atributos.
# Usar frozen=True o torna imutável, provoca um erro se algum trecho do codigo tentar altera-lo
@dataclass(frozen=True)
class Position:
    x: int
    y: int


# Responsabilidade unica (S): Verificar se a posição é valida no planalto.
@dataclass
class Grid:
    max_x: int
    max_y: int

    def is_valid_position(self, position: Position) -> bool:
        is_valid_x = 0 <= position.x <= self.max_x
        is_valid_y = 0 <= position.y <= self.max_y
        return is_valid_x and is_valid_y


# Probe é a nossa Entidade principal. Ela tem um estado e comportamento.
class Probe:
    """
    Injeção de Dependência (__init__): Note que a Probe recebe a Grid em seu construtor.
    Ela não a cria. Isso é um conceito poderoso chamado Injeção de Dependência.
    A Probe depende de uma Grid para funcionar. Ao "injetar" essa dependência, tornamos a Probe mais flexível e fácil de testar (nos testes, podemos injetar uma Grid "fake").
    """

    def __init__(self, grid: Grid, initial_direction: Direction, probe_id: str = None, initial_position: Position = Position(0, 0)):

        # A posição inicial não é maior/igual a 0 ou menor/igual ao limite?
        if not grid.is_valid_position(initial_position):
            raise InvalidMoveError(f"A posição inicial {initial_position} está fora da malha.")

        self.id: str = probe_id or str(uuid.uuid4())
        self.position: Position = initial_position
        self.direction_state: IDirectionState = DIRECTION_STATE_MAP[initial_direction]
        self.grid: Grid = grid

    @property
    def current_direction(self) -> Direction:
        """Propriedade para obter a direção atual como um Enum."""
        return self.direction_state.direction

    """
    Delegação de Lógica (turn_left, turn_right): Observe a simplicidade desses métodos. 
    A Probe não sabe a lógica de girar. Ela simplesmente delega essa responsabilidade para seu objeto de estado atual. self.direction_state = self.direction_state.turn_left(). 
    A Probe gerencia seu estado, mas os detalhes são tratados pelos especialistas (os objetos ...State).
    """

    def turn_left(self):
        """Delega a rotação para o estado de direção atual."""
        self.direction_state = self.direction_state.turn_left()
        print(f"Sonda {self.id} virou para a esquerda. Nova direção: {self.current_direction.value}")

    def turn_right(self):
        """Delega a rotação para o estado de direção atual."""
        self.direction_state = self.direction_state.turn_right()
        print(f"Sonda {self.id} virou para a direita. Nova direção: {self.current_direction.value}")

    def move(self):
        """
        Calcula a próxima posição e a valida com a malha antes de se mover.
        Levanta um erro se o movimento for inválido.
        """
        # 1. Pede ao estado atual para calcular a próxima posição
        next_x, next_y = self.direction_state.move(self.position.x, self.position.y)
        next_position = Position(x=next_x, y=next_y)

        # 2. Pede à malha para validar a próxima posição
        if not self.grid.is_valid_position(next_position):
            raise InvalidMoveError(f"Movimento para {next_position} é inválido e ultrapassa os limites da malha.")

        # 3. Se for válido, atualiza a posição
        self.position = next_position
        print(f"Sonda {self.id} moveu-se para {self.position}. Direção: {self.current_direction.value}")