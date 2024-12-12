from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.interfaces.dock_account import UpdateDockAccountRequest
from app.services.dock_account import DockAccountService

router = APIRouter(
    prefix="/dock_account",
    tags=["dock_account"],
    responses={404: {"description": "Not found"}},
)

_service = DockAccountService()

@router.get("/{cpf}")
async def get_dock_account(cpf: str):
    dock_accounts = _service.get_dock_account(cpf=cpf)
    return JSONResponse(content=jsonable_encoder(dock_accounts), status_code=200)

@router.get("/{cpf}/{_id}")
async def get_dock_account_by_id(cpf: str, _id: str):
    dock_account = _service.get_dock_account_by_id(cpf=cpf, _id=_id)
    return JSONResponse(content=jsonable_encoder(dock_account), status_code=200)

@router.post("")
async def create_dock_account(cpf: str):
    created_dock_account = _service.create(cpf=cpf)
    return JSONResponse(content=jsonable_encoder(created_dock_account), status_code=201)

@router.put("/close")
async def close_dock_account(request: UpdateDockAccountRequest):
    updated_dock_account = _service.close(request=request)
    return JSONResponse(content=jsonable_encoder(updated_dock_account), status_code=200)

@router.put("/block")
async def block_dock_account(request: UpdateDockAccountRequest):
    updated_dock_account = _service.block(request=request)
    return JSONResponse(content=jsonable_encoder(updated_dock_account), status_code=200)

@router.put("/unblock")
async def unblock_dock_account(request: UpdateDockAccountRequest):
    updated_dock_account = _service.unblock(request=request)
    return JSONResponse(content=jsonable_encoder(updated_dock_account), status_code=200)
