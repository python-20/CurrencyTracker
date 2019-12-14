import requests


json_request = requests.get(
    'https://api.exchangeratesapi.io/latest').json()

# Functions to retreive information from Json requests


def get_currencyCodes():
    currencyCodes = [c for c in json_request['rates'].keys()]
    currencyCodes.append(json_request['base'])
    return sorted(zip(currencyCodes, currencyCodes))


def get_rate(code):
    # set rate = 1 if not found, i.e. the base currency
    return json_request.get("rates").get(code, 1)


def get_base():
    return json_request['base']

# current conversion function


def conversion(amount, fromCurrency, toCurrency):
    """ Summary or Description of the Function

    Parameters:
    amount (float): The amount to be converted
    fromCurrency (string): CurrencyCode of the amount to be convered from 
    toCurrency (string): CurrencyCode of the amount to be convered to

    Returns:
    float : converted value

    """
    fromCurrencyRate = get_rate(fromCurrency)
    toCurrencyRate = get_rate(toCurrency)
    if (fromCurrency == toCurrency):
        return amount
    return round(amount * (toCurrencyRate / fromCurrencyRate), 2)
