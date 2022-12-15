from fastapi import APIRouter, Query

from api.binance import binance
from api.constants import ASSETS, FIATS


router = APIRouter(prefix="/binance", tags=["binance"])


@router.get("/paytypes/")
async def paytypes(char_code: str):
    return binance.get_paytypes(char_code=char_code)


@router.get("/assets/")
async def assets():
    return {'assets': ASSETS}


@router.get("/fiats/")
async def fiats():
    return {'fiats': FIATS}


@router.get("/assets-fiats/")
async def assets_and_fiats():
    return {
        'assets': ASSETS,
        'fiats': FIATS
    }


@router.get("/advs/")
async def advs(
    fiat: str, asset: str, trade_type: str,
    pay_types: list[str] | None = Query(default=[]),
    trans_amount: str | None = None,
    page: int = 1,
    rows: int = 10,
):
    return binance.get_advs(
        fiat=fiat,
        asset=asset,
        trade_type=trade_type,
        pay_types=pay_types,
        trans_amount=trans_amount,
        page=page,
        rows=rows,
    )

@router.get("/best_exchange_way/")
async def best_exchange_way(fiat_1: str, fiat_2: str,
    pay_types_1: list[str] | None = Query(default=[]),
    pay_types_2: list[str] | None = Query(default=[]),
    trans_amount: str | None = None, rows: int | None = 5):
    return binance.get_best_exchange_way(
        fiat_1=fiat_1,
        fiat_2=fiat_2,
        pay_types_1=pay_types_1,
        pay_types_2=pay_types_2,
        trans_amount=trans_amount,
        rows=rows,
    )