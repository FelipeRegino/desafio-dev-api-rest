import pytest
from fastapi import HTTPException
from app.repositories.holder_repository import HolderRepository
from app.database.models.holder import Holder
from app.interfaces.holder import HolderInterface

@pytest.fixture
def mock_holder():
    return HolderInterface(cpf="18046837016", name="Test Holder")

@pytest.fixture
def repository():
    return HolderRepository()

@pytest.fixture
def setup_database(mock_holder):
    # Delete the mock_holder instance before and after each test
    Holder.delete().where(Holder.cpf == mock_holder.cpf).execute()

    yield  # Allow the test to run

    Holder.delete().where(Holder.cpf == mock_holder.cpf).execute()

def test_insert_success(setup_database, repository, mock_holder):
    # Call the insert method
    result = repository.insert(mock_holder)

    # Validate the result
    assert result.cpf == mock_holder.cpf
    assert result.name == mock_holder.name

def test_insert_duplicate_holder(setup_database, repository, mock_holder):
    # Insert the holder to simulate an existing entry
    Holder.create(**mock_holder.model_dump())

    # Call the insert method and expect an HTTPException
    with pytest.raises(HTTPException) as ex:
        repository.insert(mock_holder)

    # Validate the exception
    assert ex.value.status_code == 422
    assert ex.value.detail == "Holder already exists"

def test_get_by_id_success(setup_database, repository, mock_holder):
    # Insert the holder to simulate an existing entry
    Holder.create(**mock_holder.model_dump())

    # Call the get_by_id method
    result = repository.get_by_id(cpf=mock_holder.cpf)

    # Validate the result
    assert result.cpf == mock_holder.cpf
    assert result.name == mock_holder.name

def test_get_by_id_not_found(setup_database, repository):
    # Call the get_by_id method and expect an HTTPException
    with pytest.raises(HTTPException) as ex:
        repository.get_by_id(cpf="99999999999")

    # Validate the exception
    assert ex.value.status_code == 404
