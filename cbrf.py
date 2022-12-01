import datetime
from typing import Union
import xml.etree.ElementTree as ET

import requests


def get_currency(char_code: str='KZT', return_dt: bool=False) -> Union[float, tuple[float, datetime.datetime]]:
    """Returns currency value from cbrf for selected char code

    :param char_code: currency code from cbrf (default: 'KZT') 
    :param return_df: whether return actual date of report or not 
    (default: 'False')

    :returns: depend on return_df: if True then rate with actual date and only 
    rate otherwise
    """
    req = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    if not req.ok:
        raise requests.exceptions.RequestException(f'Bad request with status code: {req.status_code}')
    tree = ET.fromstring(req.text)
    valute_items = tree.findall(f"./Valute[CharCode='{char_code.upper()}']/")
    if not len(valute_items):
        raise ValueError(f'Valute <{char_code.upper()}> is not found!')
    valute_info = {elem.tag: elem.text for elem in valute_items}
    if 'Nominal' not in valute_info or 'Value' not in valute_info:
        raise AttributeError(f"Bad xml. There are not 'Nominal' or 'Value' values!")
    rate = float(valute_info['Value'].replace(',', '.')) / int(valute_info['Nominal'])
    if return_dt:
        dt_parsed = tree.get('Date')
        dt = datetime.datetime.strptime(dt_parsed, '%d.%m.%Y').date()
        return rate, dt
    return rate


if __name__ == '__main__':
    char_codes = ['USD', 'KZT', 'LOL']

    for char_code in char_codes:
        print(char_code, ' - ', end='')
        rate, dt = get_currency(char_code=char_code, return_dt=True)
        print(rate, f'({dt})')
