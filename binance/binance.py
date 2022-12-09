from typing import Any, Union, Literal

import requests


# default type of API answer
API_answer = dict[str: Any]
# header for BinanceAPI
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
}
# BinanceAPI url
API_URL: str = 'https://p2p.binance.com/bapi/c2c/v2/{api_type}/c2c/adv/'
# Available binance P2P assets
ASSETS: list[str] = ["USDT", "BTC", "BNB", "BUSD", "ETH"]
# Available binance P2P fiats
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

def get_exchange_rate(from_currency: str='KZT', 
    to_currency: str='RUB') -> API_answer:
    """Returns currency value from one valute to another

    :param from_currency: first valute char code (default: 'KZT') 
    :param to_currency: second valute char code (default: 'RUB')

    :returns: data with currency rate
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    data = {
        'from': from_currency,
        'to': to_currency,
    }

    if from_currency not in FIATS or to_currency not in FIATS:
        data['succes'] = False
        return data

    if from_currency == to_currency:
        data['rate'] = 1.0
        data['success'] = True
        return data

    API_URL: str = "https://currency-exchange.p.rapidapi.com/exchange"

    querystring = data.copy()
    querystring['q'] = "1.0"
    headers = {
        "X-RapidAPI-Key": "e56577286emshfab6972cb48107ap1e3e26jsn1fa773c36844",
        "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
    }

    try:
        response = requests.request(
            method="GET", 
            url=API_URL,
            headers=headers, 
            params=querystring,
            timeout=7
        )
        if response.ok:
            try:
                data['rate'] = float(response.text)
            except (ValueError, TypeError):
                data['rate'] = None
            else:
                data['success'] = True
    except requests.exceptions.ReadTimeout:
        data['success'] = False

    return data

def get_paytypes(char_code: str) -> API_answer:
    """Availiable Binance payment methods for p2p trading

    :param char_code: valute char code (3 symbols)

    :returns: data with paytypes list
    """
    data = {}
    try:
        paytypes = []
        response = requests.post(
            API_URL.format(api_type='public') + 'filter-conditions', 
            headers=HEADERS, 
            json={'fiat': char_code.upper()}
        ).json()
        if not response.ok:
            raise requests.exceptions.RequestException
        for trade_method in response['data']['tradeMethods']:
            paytypes.append(trade_method['identifier'])
        if not len(paytypes):
            raise ValueError
        data['paytypes'] = paytypes
        data['succes'] = True
    except Exception:
        data['success'] = False
    return data

def get_advs(fiat: str, asset: str, trade_type: Literal["BUY", "SELL"], 
    pay_types: list[str]=[], trans_amount: Union[str, None]=None, page: int=1,
    rows: int=10) -> API_answer:
    """Actual bids from BinanceP2P

    :param fiat: fiat name (char_code)
    :param asset: asset name (char_code)
    :param trade_type: BUY or SELL
    :param pay_types: available payment methods
    :param trans_amout: required transaction amount
    :param page: page number (binance pagination)
    :param rows: number of rows per one page

    :returns: data with bid's information
    """
    data = {"advs": []}
    # TODO: add try block
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
            data['advs'].append({
                'advNo': adv['adv']['advNo'],
                'tradeType': 'SELL' 
                    if adv['adv']['tradeType'] == 'BUY' else 'BUY',
                'asset': adv['adv']['asset'],
                'fiatUnit': adv['adv']['fiatUnit'],
                'price': adv['adv']['price'],
                'minTransAmount': adv['adv']['minSingleTransAmount'],
                'maxTransAmount': adv['adv']['dynamicMaxSingleTransAmount'],
                'tradeMethods': [
                    pay_type['identifier'] 
                        for pay_type in adv['adv']['tradeMethods']
                ],
                'tradableQuantity': adv['adv']['tradableQuantity'],
                'advertiserName': adv['advertiser']['nickName'],
                'monthOrderCount': adv['advertiser']['monthOrderCount'],
                'monthFinishRate': adv['advertiser']['monthFinishRate'],
                
            })
        data['totalCount'] = response['total']
    data['success'] = response['success']
    return data

def _weighted_mean_price(data: Any, price_key='price', 
    weight_key='tradableQuantity') -> float:
    return sum(float(adv[price_key]) * float(adv[weight_key]) \
        for adv in data['advs']) /\
        sum(float(adv[weight_key]) for adv in data['advs'])

def get_best_exchange_way(fiat_1: str, fiat_2: str, pay_types_1: list[str]=[],
    pay_types_2: list[str]=[], trans_amount: Union[str, None]=None, 
    rows: int=5) -> API_answer:
    """Show best exchange way for required pair of curriencies

    :param fiat_1: first fiat name (char_code)
    :param fiat_2: second fiat name (char_code)
    :param pay_types_1: available payment methods for fiat_1
    :param pay_types_2: available payment methods for fiat_2
    :param trans_amout: required transaction amount (for fiat_1)

    :returns: data with table of all assets and best exchange way
    """
    """
    data
        -
    """
    exchange_rate = get_exchange_rate(
        from_currency=fiat_2,
        to_currency=fiat_1,
    )['rate']
    data = {
        'table': {
            'asset': [],
            f'{fiat_1.upper()}': [],
            f'{fiat_2.upper()}': [],
            f'{fiat_1.upper()}/{fiat_2.upper()}': [],
            'market_diff': [],
        },
        'rate': exchange_rate,
    }
    
    # get best (appropriate) bid for each asset
    for asset in ASSETS:
        data_buy = get_advs(
            fiat=fiat_1,
            asset=asset,
            trade_type='BUY',
            pay_types=pay_types_1,
            trans_amount=int(trans_amount),
            page=1,
            rows=rows,
        )
        if not len(data_buy['advs']):
            continue
        
        data_sell = get_advs(
            fiat=fiat_2,
            asset=asset,
            trade_type='SELL',
            pay_types=pay_types_2,
            trans_amount=int(int(trans_amount) / exchange_rate) + 1,
            page=1,
            rows=rows,
        )
        if not len(data_sell['advs']):
            continue

        price_buy = _weighted_mean_price(data_buy)
        price_sell = _weighted_mean_price(data_sell)

        data['table']['asset'].append(asset)
        data['table'][f'{fiat_1.upper()}'].append(price_buy)
        data['table'][f'{fiat_2.upper()}'].append(price_sell)
        data['table'][f'{fiat_1.upper()}/{fiat_2.upper()}'].append(
            price_buy / price_sell
        )
        data['table']['market_diff'].append(
            price_buy / price_sell / exchange_rate - 1
        )

    if len(data['table']['asset']):
        data['success'] = True
    else:
        data['succes'] = False

    return data



if __name__ == '__main__':
    for fiat in FIATS:
        rate = get_exchange_rate('RUB', 'KZT')
        print(rate)