import pytest
from app.domain.models import Grid, Probe, Position, InvalidMoveError
from app.domain.state import Direction


# --- Testes para a classe Grid ---

# Teste para verificar se a Grid reconhece posições válidas
def test_grid_should_know_when_a_position_is_valid():
    # Arrange (Organizar)
    grid = Grid(max_x=5, max_y=5)
    valid_position = Position(x=3, y=4)

    # Act (Agir)
    is_valid = grid.is_valid_position(valid_position)

    # Assert (Verificar)
    assert is_valid is True

# Teste para verificar se a Grid reconhece posições inválidas
def test_grid_should_know_when_a_position_is_invalid():
    # Arrange
    grid = Grid(max_x=5, max_y=5)
    invalid_position_x = Position(x=6, y=5)
    invalid_position_y = Position(x=5, y=6)

    # Act & Assert
    assert grid.is_valid_position(invalid_position_x) is False
    assert grid.is_valid_position(invalid_position_y) is False
    assert grid.is_valid_position(Position(x=-1, y=0)) is False


# --- Testes para a classe Probe ---

@pytest.fixture
def default_grid():
    """Cria uma Grid padrão para ser usada em múltiplos testes."""
    return Grid(max_x=5, max_y=5)

# Teste para verificar se a sonda gira corretamente para a esquerda (INICIA APONTANDO PARA CIMA - NORTH)
def test_probe_should_turn_left_correctly(default_grid):
    # Arrange
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

    # Act: North -> West -> South -> East -> North
    probe.turn_left()
    assert probe.current_direction == Direction.WEST

    probe.turn_left()
    assert probe.current_direction == Direction.SOUTH

    probe.turn_left()
    assert probe.current_direction == Direction.EAST

    probe.turn_left()
    assert probe.current_direction == Direction.NORTH

# Teste para verificar se a sonda gira corretamente para a direita (INICIA APONTANDO PARA CIMA - NORTH)
def test_probe_should_turn_right_correctly(default_grid):
    # Arrange
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

    # Act: North -> East -> South -> West -> North
    probe.turn_right()
    assert probe.current_direction == Direction.EAST

    probe.turn_right()
    assert probe.current_direction == Direction.SOUTH

    probe.turn_right()
    assert probe.current_direction == Direction.WEST

    probe.turn_right()
    assert probe.current_direction == Direction.NORTH

# Teste para verificar se a sonda se move corretamente dentro dos limites da grade
def test_probe_should_move_forward_correctly(default_grid):
    # Arrange
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

    # Act
    probe.move()  # Move para (0, 1)

    # Assert
    assert probe.position == Position(x=0, y=1)

    # Arrange 2
    probe.turn_right()  # Agora aponta para EAST

    # Act 2
    probe.move()  # Move para (1, 1)

    # Assert 2
    assert probe.position == Position(x=1, y=1)

# Teste para verificar se a sonda levanta um erro ao tentar se mover fora dos limites da grade
def test_probe_should_raise_error_when_moving_outside_grid_limits(default_grid):
    # Arrange - Sonda no canto superior esquerdo (0, 5), apontando para o Norte
    probe = Probe(
        grid=default_grid,
        initial_position=Position(x=0, y=5),
        initial_direction=Direction.NORTH
    )

    # Act & Assert
    # Verificamos se a exceção InvalidMoveError é levantada ao tentar mover
    with pytest.raises(InvalidMoveError) as excinfo:
        probe.move()

    # Opcional: Verificar a mensagem de erro para ter certeza que é a correta
    assert "ultrapassa os limites da malha" in str(excinfo.value)

    # Garantir que a posição da sonda não mudou
    assert probe.position == Position(x=0, y=5)