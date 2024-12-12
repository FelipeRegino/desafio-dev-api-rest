import re

from fastapi import HTTPException

from app.interfaces.dock_account import DockAccountInterface, UpdateDockAccountRequest
from app.interfaces.enum import AccountStatus
from app.repositories.dock_account_repository import DockAccountRepository
from app.repositories.holder_repository import HolderRepository
from app.utils.generator import generate_random_account_number, generate_random_agency_number

class DockAccountService:
    def __init__(self):
        self._repository = DockAccountRepository()
        self._holder_repository = HolderRepository()

    def get_dock_account(self, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        accounts = self._holder_repository.get_holder_accounts(cpf=cpf)
        return accounts

    def get_dock_account_by_id(self, cpf: str, _id: str):
        cpf = re.sub("[^0-9]", "", cpf)
        account = self._repository.get_by_id(_id=_id, holder=cpf)
        return account

    def create(self, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        holder = self._holder_repository.get_by_id(cpf=cpf, **{"status": True})
        dock_account = DockAccountInterface(
            holder=holder.cpf,
            number=generate_random_account_number(),
            agency=generate_random_agency_number()
        )
        new_dock_account = self._repository.insert(dock_account=dock_account)
        return new_dock_account

    def close(self, request: UpdateDockAccountRequest):
        dock_account = self._repository.get_by_id(_id=request.id, holder=request.cpf)
        if dock_account.status == AccountStatus.closed:
            raise HTTPException(status_code=422, detail="DockAccount is already closed")
        dock_account.status = AccountStatus.closed
        updated_dock_account = self._repository.update(dock_account=dock_account)
        return updated_dock_account

    def block(self, request: UpdateDockAccountRequest):
        dock_account = self._repository.get_by_id(_id=request.id, holder=request.cpf)
        if dock_account.status == AccountStatus.blocked:
            raise HTTPException(status_code=422, detail="DockAccount is already blocked")
        elif dock_account.status == AccountStatus.closed:
            raise HTTPException(status_code=422, detail="DockAccount is closed")
        dock_account.status = AccountStatus.blocked
        updated_dock_account = self._repository.update(dock_account=dock_account)
        return updated_dock_account

    def unblock(self, request: UpdateDockAccountRequest):
        dock_account = self._repository.get_by_id(_id=request.id, holder=request.cpf)
        if dock_account.status == AccountStatus.active:
            raise HTTPException(status_code=422, detail="DockAccount is already unblocked")
        elif dock_account.status == AccountStatus.closed:
            raise HTTPException(status_code=422, detail="DockAccount is closed")
        dock_account.status = AccountStatus.active
        updated_dock_account = self._repository.update(dock_account=dock_account)
        return updated_dock_account
