import json


def get_exchange_rate(currency_pair: str) -> str:
    """
    Get the exchange rate for a given currency pair.
    """
    rates = {
        "USD_TWD": "32.0",
        "JPY_TWD": "0.2",
        "EUR_USD": "1.2",
    }
    if currency_pair in rates:
        return json.dumps(
            {"currency_pair": currency_pair, "rate": rates[currency_pair]}
        )
    return json.dumps({"error": "Data not found"})


def get_stock_price(symbol: str) -> str:
    """
    Get the stock price for a given symbol.
    """
    prices = {
        "AAPL": "260.00",
        "TSLA": "430.00",
        "NVDA": "190.00",
    }
    if symbol in prices:
        return json.dumps({"symbol": symbol, "price": prices[symbol]})
    return json.dumps({"error": "Data not found"})
