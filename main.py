from typing import Union

from fastapi import FastAPI, HTTPException, Query

from binance import ASSETS, FIATS, get_advs, get_paytypes
from cbrf import get_currency

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/currency/")
async def currency(char_code: str, date: bool = False):
    dt = 'null'
    try:
        if not date:
            currency_ = get_currency(char_code=char_code)
        else:
            currency_, dt = get_currency(char_code=char_code, return_dt=date)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    return {f'{char_code.upper()}': currency_, 'date': str(dt)}


@app.get("/paytypes/")
async def paytypes(char_code: str):
    paytypes = get_paytypes(char_code=char_code)
    if not len(paytypes):
        raise HTTPException(status_code=404, detail='Currency not found.')
    return {'paytypes': paytypes}


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
    page: int=1,
    rows: int=10,
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
