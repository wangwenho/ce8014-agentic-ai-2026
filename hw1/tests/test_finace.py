import json

from tools.finance import get_exchange_rate, get_stock_price


def test_exchange_rate_known():
    res = json.loads(get_exchange_rate("USD_TWD"))
    assert res["currency_pair"] == "USD_TWD"
    assert res["rate"] == "32.0"


def test_exchange_rate_unknown():
    res = json.loads(get_exchange_rate("ABC_XYZ"))
    assert res == {"error": "Data not found"}


def test_stock_price_known():
    res = json.loads(get_stock_price("AAPL"))
    assert res["symbol"] == "AAPL"
    assert res["price"] == "260.00"


def test_stock_price_unknown():
    res = json.loads(get_stock_price("GOOG"))
    assert res == {"error": "Data not found"}
