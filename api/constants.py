from typing import Any


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