from typing import List

from fastapi import HTTPException
from playhouse.shortcuts import model_to_dict

from app.database.models.holder import Holder
from app.interfaces.dock_account import DockAccountInterface
from app.interfaces.holder import HolderInterface


class HolderRepository:
    def __init__(self):
        self._model = Holder

    def insert(self, holder: HolderInterface) -> HolderInterface:
        if self._model.select().where(self._model.cpf == holder.cpf).first():
            raise HTTPException(status_code=422, detail="Holder already exists")
        inserted_holder = self._model.create(**holder.model_dump())
        return HolderInterface(**model_to_dict(inserted_holder))

    def get_by_id(self, cpf: str, **filters) -> HolderInterface:
        holder = self._model.select().where(self._model.cpf == cpf)
        if filters:
            holder = holder.filter(**filters)
        holder = holder.first()
        if not holder:
            raise HTTPException(status_code=404, detail="Holder not found")
        return HolderInterface(**model_to_dict(holder))

    def get_holder_accounts(self, cpf: str) -> List[DockAccountInterface]:
        holder = self._model.select().where(self._model.cpf == cpf).first()
        return [DockAccountInterface.build(dock_account=x) for x in holder.accounts]

    def update(self, holder: HolderInterface) -> HolderInterface:
        holder_to_update = self._model.select().where(self._model.cpf == holder.cpf).first()
        if not holder_to_update:
            raise HTTPException(status_code=404, detail="Holder not found")
        holder_to_update.update(**holder.model_dump()).where(self._model.cpf == holder.cpf).execute()
        return holder
