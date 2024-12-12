from datetime import datetime

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.interfaces.transaction_history import TransactionHistoryInterface
from app.services.transaction_history import TransactionHistoryService

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)

_service = TransactionHistoryService()

@router.get("/{dock_account_id}")
async def get_transaction_history(dock_account_id: str, start_date: datetime = None, end_date: datetime = None):
    transaction_history = _service.get_transaction_history(
        dock_account_id=dock_account_id, start_date=start_date, end_date=end_date
    )
    return JSONResponse(content=jsonable_encoder(transaction_history), status_code=200)

@router.post("")
async def create_transaction(transaction_history: TransactionHistoryInterface):
    created_transaction_history = _service.create(transaction_history=transaction_history)
    return JSONResponse(content=jsonable_encoder(created_transaction_history), status_code=201)
