from typing import Union

import requests


HEADERS: dict[str, str] = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "123",
            "content-type": "application/json",
            "Host": "p2p.binance.com",
            "Origin": "https://p2p.binance.com",
            "Pragma": "no-cache",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}
API_URL: str = 'https://p2p.binance.com/bapi/c2c/v2/{api_type}/c2c/adv/'

ASSETS: list[str] = ["USDT", "BTC", "BNB", "BUSD", "ETH"]
FIATS: list[str] = [
    "AED", "AFN", "AMD", "ARS", "AUD", "AZN", "BDT", "BGN", "BHD", "BIF", "BND",
    "BOB", "BRL", "CAD", "CHF", "CLP", "CNY", "COP", "CRC", "CZK", "DJF", "DKK",
    "DOP", "DZD", "EGP", "ETB", "EUR", "GBP", "GEL", "GHS", "GNF", "GTQ", "HKD",
    "HNL", "HRK", "HUF", "IDR", "INR", "ISK", "JOD", "JPY", "KES", "KGS", "KHR",
    "KMF", "KWD", "KZT", "LAK", "LBP", "LKR", "LYD", "MAD", "MDL", "MGA", "MMK",
    "MNT", "MOP", "MXN", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN",
    "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR",
    "SCR", "SDG", "SEK", "THB", "TJS", "TMT", "TND", "TRY", "TWD", "TZS", "UAH",
    "UGX", "USD", "UYU", "UZS", "VES", "VND", "XAF", "XOF", "YER", "ZAR",
]

def get_paytypes(char_code: str) -> list[str]:
    paytypes = []
    response = requests.post(
        API_URL.format(api_type='public') + 'filter-conditions', 
        headers=HEADERS, 
        json={'fiat': char_code.upper()}
    ).json()
    for trade_method in response['data']['tradeMethods']:
        paytypes.append(trade_method['identifier'])
    return paytypes

def get_advs(fiat: str, asset: str, trade_type: str, pay_types: list[str]=[],
    trans_amount: Union[str, None]=None, page: int=1, rows: int=10):
    advs = {"advs": []}
    response = requests.post(
        API_URL.format(api_type='friendly') + 'search', 
        headers=HEADERS, 
        json={
            "page": page,
            "rows": rows,
            "payTypes": pay_types,
            "transAmount": trans_amount,
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type
        }
    ).json()
    if response.get('data') is not None:
        for adv in response['data']:
            advs['advs'].append({
                'advNo': adv['adv']['advNo'],
                'tradeType': 'SELL' if adv['adv']['tradeType'] == 'BUY' else 'BUY',
                'asset': adv['adv']['asset'],
                'fiatUnit': adv['adv']['fiatUnit'],
                'price': adv['adv']['price'],
                'minTransAmount': adv['adv']['minSingleTransAmount'],
                'maxTransAmount': adv['adv']['dynamicMaxSingleTransAmount'],
                'tradeMethods': [
                    pay_type['identifier'] for pay_type in adv['adv']['tradeMethods']
                ],
                'tradableQuantity': adv['adv']['tradableQuantity'],
                'advertiserName': adv['advertiser']['nickName'],
                'monthOrderCount': adv['advertiser']['monthOrderCount'],
                'monthFinishRate': adv['advertiser']['monthFinishRate'],
                
            })
        advs['totalCount'] = response['total']
    advs['success'] = response['success']
    return advs

def best_exchange_way(fiat_1: str, fiat_2: str, pay_types_1: list[str]=[],
    pay_types_2: list[str]=[], trans_amount: Union[str, None]=None
):
    advs1 = get_advs(
        fiat=fiat_1,
        asset=asset,
        trade_type=trade_type,
        pay_types=pay_types,
        trans_amount=trans_amount,
        page=page,
        rows=rows,
    )