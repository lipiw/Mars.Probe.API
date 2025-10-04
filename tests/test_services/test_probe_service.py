import pytest
from unittest.mock import Mock

from app.services.probe_service import ProbeService, ProbeNotFoundError, InvalidCommandError
from app.domain.models import Probe, Grid
from app.domain.state import Direction

# Teste para verificar o lançamento de uma nova Probe
def test_launch_probe_should_save_a_new_probe():
    mock_repo = Mock()

    service = ProbeService(probe_repository=mock_repo)

    launched_probe = service.launch_probe(max_x=5, max_y=5, direction_str="NORTH")

    mock_repo.save.assert_called_once()

    assert launched_probe.position.x == 0
    assert launched_probe.position.y == 0
    assert launched_probe.current_direction == Direction.NORTH

# Teste para verificar a movimentação de uma Probe
def test_move_probe_should_succeed_and_save_final_state():
    probe_id = "test-id"
    initial_probe = Probe(
        probe_id=probe_id,
        grid=Grid(5, 5),
        initial_direction=Direction.NORTH
    )

    mock_repo = Mock()
    mock_repo.get_by_id.return_value = initial_probe

    service = ProbeService(probe_repository=mock_repo)

    final_probe = service.move_probe(probe_id=probe_id, commands="MRM")

    mock_repo.get_by_id.assert_called_once_with(probe_id)

    assert final_probe.position.x == 1
    assert final_probe.position.y == 1
    assert final_probe.current_direction == Direction.EAST

    mock_repo.save.assert_called_once_with(final_probe)

# Teste para verificar o erro de uma movimentação de uma Probe que não existe
def test_move_probe_should_raise_error_if_probe_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = None

    service = ProbeService(probe_repository=mock_repo)

    with pytest.raises(ProbeNotFoundError):
        service.move_probe(probe_id="non-existent-id", commands="M")

    mock_repo.save.assert_not_called()

# Teste para verificar o erro de uma movimentação invalida
def test_move_probe_should_raise_error_and_not_save_on_invalid_move():
    probe_id = "test-id"
    initial_probe = Probe(
        probe_id=probe_id,
        grid=Grid(5, 5),
        initial_direction=Direction.NORTH,
        initial_position=pytest.importorskip("app.domain.models").Position(0, 5)
    )

    mock_repo = Mock()
    mock_repo.get_by_id.return_value = initial_probe

    service = ProbeService(probe_repository=mock_repo)

    with pytest.raises(InvalidCommandError):
        service.move_probe(probe_id=probe_id, commands="M")

    mock_repo.save.assert_not_called()