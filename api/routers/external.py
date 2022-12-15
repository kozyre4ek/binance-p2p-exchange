from fastapi import APIRouter

from api.external.exchange_rate import get_exchange_rate


router = APIRouter(prefix="/external", tags=['external'])

@router.get("/exchange_rate/")
async def exchange_rate(from_currency: str, to_currency: str):
    return get_exchange_rate(from_currency, to_currency)