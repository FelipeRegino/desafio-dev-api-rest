from fastapi import HTTPException

from app.interfaces.holder import HolderInterface
from app.repositories.holder_repository import HolderRepository
from app.utils.validator import validate_cpf


class HolderService:
    def __init__(self):
        self._repository = HolderRepository()

    def get_holder(self, cpf: str):
        holder = self._repository.get_by_id(cpf=cpf)
        return holder

    def create(self, holder: HolderInterface):
        cpf = validate_cpf(holder.cpf)
        if not cpf:
            raise HTTPException(status_code=422, detail="Invalid CPF")
        holder.cpf = cpf
        new_holder = self._repository.insert(holder=holder)
        return new_holder

    def update(self, holder: HolderInterface):
        updated_holder = self._repository.update(holder=holder)
        return updated_holder
