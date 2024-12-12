import pytest
from fastapi.testclient import TestClient
from app.database.models.holder import Holder
from app.http_server import app
from app.interfaces.holder import HolderInterface

client = TestClient(app)

@pytest.fixture
def mock_holder():
    return HolderInterface(
        cpf="83463794047",
        name="Test Holder"
    )

@pytest.fixture
def setup_database(mock_holder):
    # Delete any existing holder with the mock CPF before and after each test
    Holder.delete().where(Holder.cpf == mock_holder.cpf).execute()

    yield  # Allow the test to run

    Holder.delete().where(Holder.cpf == mock_holder.cpf).execute()

def test_get_holder_success(setup_database, mock_holder):
    # Create a holder in the database
    Holder.create(**mock_holder.model_dump())

    # Call the GET /holder/{cpf} endpoint
    response = client.get(f"/holder/{mock_holder.cpf}")

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["cpf"] == mock_holder.cpf
    assert data["name"] == mock_holder.name

def test_get_holder_not_found():
    # Call the GET /holder/{cpf} endpoint for a non-existing CPF
    response = client.get("/holder/99999999999")

    # Validate the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Holder not found"

def test_create_holder_success(setup_database, mock_holder):
    # Call the POST /holder endpoint
    response = client.post("/holder", json=mock_holder.model_dump())

    # Validate the response
    assert response.status_code == 201
    data = response.json()
    assert data["cpf"] == mock_holder.cpf
    assert data["name"] == mock_holder.name

def test_create_holder_invalid():
    # Call the POST /holder endpoint with invalid data
    response = client.post("/holder", json={"cpf": "", "name": ""})

    # Validate the response
    assert response.status_code == 422

def test_deactivate_holder_success(setup_database, mock_holder):
    # Create a holder in the database
    Holder.create(**mock_holder.model_dump())

    # Call the PUT /holder endpoint
    response = client.put("/holder/deactivate", json={"cpf": mock_holder.cpf})

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Holder deactivated"
