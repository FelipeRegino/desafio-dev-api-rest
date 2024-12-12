from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.interfaces.holder import HolderInterface
from app.services.holder import HolderService

router = APIRouter(
    prefix="/holder",
    tags=["holder"],
    responses={404: {"description": "Not found"}},
)

_service = HolderService()

@router.get("/{cpf}")
async def get_holder(cpf: str):
    holder = _service.get_holder(cpf=cpf)
    return JSONResponse(content=jsonable_encoder(holder), status_code=200)

@router.post("")
async def create_holder(holder: HolderInterface):
    created_holder = _service.create(holder=holder)
    return JSONResponse(content=jsonable_encoder(created_holder), status_code=201)

@router.put("")
async def update_holder(holder: HolderInterface):
    updated_holder = _service.update(holder=holder)
    return JSONResponse(content=jsonable_encoder(updated_holder), status_code=200)
