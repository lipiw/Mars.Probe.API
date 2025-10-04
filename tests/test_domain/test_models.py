import pytest
from app.domain.models import Grid, Probe, Position, InvalidMoveError
from app.domain.state import Direction


# Teste para verificar se a Grid reconhece posições válidas
def test_grid_should_know_when_a_position_is_valid():
    grid = Grid(max_x=5, max_y=5)
    valid_position = Position(x=3, y=4)

    is_valid = grid.is_valid_position(valid_position)

    assert is_valid is True

# Teste para verificar se a Grid reconhece posições inválidas
def test_grid_should_know_when_a_position_is_invalid():
    grid = Grid(max_x=5, max_y=5)
    invalid_position_x = Position(x=6, y=5)
    invalid_position_y = Position(x=5, y=6)

    assert grid.is_valid_position(invalid_position_x) is False
    assert grid.is_valid_position(invalid_position_y) is False
    assert grid.is_valid_position(Position(x=-1, y=0)) is False


# --- Testes para a classe Probe ---

@pytest.fixture
def default_grid():
    return Grid(max_x=5, max_y=5)

# Teste para verificar se a sonda gira corretamente para a esquerda (INICIA APONTANDO PARA CIMA - NORTH)
def test_probe_should_turn_left_correctly(default_grid):
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

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
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

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
    probe = Probe(grid=default_grid, initial_direction=Direction.NORTH)

    probe.move()

    assert probe.position == Position(x=0, y=1)

    probe.turn_right()

    probe.move()

    assert probe.position == Position(x=1, y=1)

# Teste para verificar se a sonda levanta um erro ao tentar se mover fora dos limites da grade
def test_probe_should_raise_error_when_moving_outside_grid_limits(default_grid):
    probe = Probe(
        grid=default_grid,
        initial_position=Position(x=0, y=5),
        initial_direction=Direction.NORTH
    )

    with pytest.raises(InvalidMoveError) as excinfo:
        probe.move()

    assert "ultrapassa os limites da malha" in str(excinfo.value)

    assert probe.position == Position(x=0, y=5)