# tests/test_operation.py
import pytest
from fastapi.testclient import TestClient
from main import create_app
from app.operation.schema import OperationCreateSchema
from app.operation.model import OperationEntity

@pytest.fixture
def client():
    app = create_app()
    client = TestClient(app)
    return client

def test_create_operation(client):
    operation_data = OperationCreateSchema(
        amount_required=1000.0,
        title="Prueba de operación",
        description="Esta es una prueba de operación",
        annual_interest=5.0,
        deadline="2024-12-31",
        is_closed=False,
        operator_id=1,
        status_id=1
    )
    response = client.post("/operation/", json=operation_data.dict())
    assert response.status_code == 201
    assert response.json()["title"] == operation_data.title

def test_get_all_operations(client):
    response = client.get("/operation/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_operation_by_id(client):
    operation_id = 1
    response = client.get(f"/operation/{operation_id}")
    assert response.status_code == 200
    assert response.json()["id"] == operation_id

def test_update_operation(client):
    operation_id = 1
    operation_data = OperationCreateSchema(
        amount_required=2000.0,
        title="Prueba de operación actualizada",
        description="Esta es una prueba de operación actualizada",
        annual_interest=6.0,
        deadline="2025-12-31",
        is_closed=False,
        operator_id=1,
        status_id=1
    )
    response = client.put(f"/operation/{operation_id}", json=operation_data.dict())
    assert response.status_code == 200
    assert response.json()["title"] == operation_data.title

def test_delete_operation(client):
    operation_id = 1
    response = client.delete(f"/operation/{operation_id}")
    assert response.status_code == 204