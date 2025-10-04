import pytest
from fastapi.testclient import TestClient

from main import app
from app.api.endpoints.dependencies import get_probe_service
from app.services.probe_service import ProbeService
from app.repositories.probe_repository import InMemoryProbeRepository


# --- Configuração do Ambiente de Teste ---

@pytest.fixture
def client_with_clean_db():
    test_repo = InMemoryProbeRepository()
    test_service = ProbeService(probe_repository=test_repo)

    def get_test_probe_service():
        return test_service

    app.dependency_overrides[get_probe_service] = get_test_probe_service

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


# Teste para verificar o lançamento de uma Sonda via API
def test_launch_probe_success(client_with_clean_db):
    client = client_with_clean_db
    request_body = {"x": 5, "y": 5, "direction": "NORTH"}

    response = client.post("/api/probes", json=request_body)

    assert response.status_code == 201
    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 0
    assert data["direction"] == "NORTH"
    assert "id" in data

# Teste para verificar a recuperação de todas Sondas
def test_get_all_probes_returns_list(client_with_clean_db):
    client = client_with_clean_db
    client.post("/api/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    client.post("/api/probes", json={"x": 10, "y": 10, "direction": "SOUTH"})

    response = client.get("/api/probes")

    assert response.status_code == 200
    data = response.json()
    assert "probes" in data
    assert len(data["probes"]) == 2

# Teste para verificar a movimentação de uma Sonda
def test_move_probe_success(client_with_clean_db):
    client = client_with_clean_db
    launch_response = client.post("/api/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    probe_id = launch_response.json()["id"]

    move_body = {"commands": "MRM"}

    move_response = client.post(f"/api/probes/{probe_id}/move", json=move_body)

    assert move_response.status_code == 200
    data = move_response.json()
    assert data["x"] == 1
    assert data["y"] == 1
    assert data["direction"] == "EAST"

# Teste para verificar a existencia de uma Sonda (ERRO)
def test_move_probe_not_found_returns_404(client_with_clean_db):
    client = client_with_clean_db

    response = client.post("/api/probes/fake-id-123/move", json={"commands": "M"})

    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]

# Teste para verificar a movimentação de uma Sonda (ERRO)
def test_move_probe_off_grid_returns_400(client_with_clean_db):
    client = client_with_clean_db
    launch_response = client.post("/api/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    probe_id = launch_response.json()["id"]

    move_response = client.post(f"/api/probes/{probe_id}/move", json={"commands": "MMMMMM"})

    assert move_response.status_code == 400
    assert "movimento inválido" in move_response.json()["detail"]