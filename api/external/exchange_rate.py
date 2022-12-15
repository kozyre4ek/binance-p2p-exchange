import requests

from ..constants import API_answer, FIATS

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