import pytest
from fastapi import HTTPException
from app.services.holder import HolderService
from app.interfaces.holder import HolderInterface
from app.repositories.holder_repository import HolderRepository


@pytest.fixture(scope="module")
def holder_service():
    return HolderService()

@pytest.fixture(scope="module")
def holder_repository():
    return HolderRepository()

def test_get_holder_success(holder_service, holder_repository):
    # Prepare data in the database
    holder_repository.insert(HolderInterface(cpf="38233752029", name="Test User"))

    # Call the service method
    result = holder_service.get_holder(cpf="38233752029")

    # Assert the result
    assert result.cpf == "38233752029"
    assert result.name == "Test User"

def test_get_holder_not_found(holder_service):
    # Call the service method and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        # Call the service method with a non-existing CPF
        holder_service.get_holder(cpf="00000000000")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Holder not found"

def test_create_holder_success(holder_service, holder_repository):
    # Prepare the holder input
    holder = HolderInterface(cpf="802.337.610-12", name="Test User")

    # Call the service method
    result = holder_service.create(holder=holder)

    # Assert the result
    assert result.cpf == "80233761012"
    assert result.name == "Test User"

def test_create_holder_invalid_cpf(holder_service):
    # Prepare the holder input with an invalid CPF
    holder = HolderInterface(cpf="invalid_cpf", name="Test User")

    # Call the service method and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        holder_service.create(holder=holder)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid CPF"

def test_deactivate_holder(holder_service, holder_repository):
    # Insert initial data into the database
    holder_repository.insert(HolderInterface(cpf="41762501007", name="Test User"))

    # Call the service method
    holder_service.deactivate(cpf="41762501007")

    holder = holder_service.get_holder(cpf="41762501007")
    # Assert the result
    assert holder.status == False