from typing import Union

from fastapi import FastAPI, Query

from binance.binance import ASSETS, FIATS, get_best_exchange_way, get_advs, \
    get_paytypes, get_exchange_rate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exchange_rate/")
async def exchange_rate(from_currency: str, to_currency: str):
    return get_exchange_rate(from_currency, to_currency)


@app.get("/paytypes/")
async def paytypes(char_code: str):
    return get_paytypes(char_code=char_code)


@app.get("/assets/")
async def assets():
    return {'assets': ASSETS}


@app.get("/fiats/")
async def fiats():
    return {'fiats': FIATS}


@app.get("/assets-fiats/")
async def assets_and_fiats():
    return {
        'assets': ASSETS,
        'fiats': FIATS
    }


@app.get("/advs/")
async def advs(
    fiat: str, asset: str, trade_type: str,
    pay_types: Union[list[str], None] = Query(default=[]),
    trans_amount: Union[str, None] = None,
    page: int = 1,
    rows: int = 10,
):
    return get_advs(
        fiat=fiat,
        asset=asset,
        trade_type=trade_type,
        pay_types=pay_types,
        trans_amount=trans_amount,
        page=page,
        rows=rows,
    )

@app.get("/best_exchange_way/")
async def best_exchange_way(fiat_1: str, fiat_2: str,
    pay_types_1: Union[list[str], None] = Query(default=[]),
    pay_types_2: Union[list[str], None] = Query(default=[]),
    trans_amount: Union[str, None] = None, rows: int=5):
    return get_best_exchange_way(
        fiat_1=fiat_1,
        fiat_2=fiat_2,
        pay_types_1=pay_types_1,
        pay_types_2=pay_types_2,
        trans_amount=trans_amount,
        rows=rows,
    )