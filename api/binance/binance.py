from typing import Any, Literal

import requests

from ..constants import API_answer, API_URL, HEADERS, ASSETS
from ..external.exchange_rate import get_exchange_rate


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
        )
        if not response.ok:
            raise requests.exceptions.RequestException
        for trade_method in response.json()['data']['tradeMethods']:
            paytypes.append(trade_method['identifier'])
        if not len(paytypes):
            raise ValueError
        data['paytypes'] = paytypes
        data['succes'] = True
    except Exception as ex:
        print(ex)
        data['success'] = False
    return data

def get_advs(fiat: str, asset: str, trade_type: Literal["BUY", "SELL"], 
    pay_types: list[str]=[], trans_amount: str | None = None, page: int=1,
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
    pay_types_2: list[str]=[], trans_amount: str | None = None, 
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