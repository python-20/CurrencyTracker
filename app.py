from flask import Flask, render_template, request
import requests

# import config

app = Flask(__name__)
app.config['DEBUG'] = True

json_request = requests.get(
    'https://api.exchangeratesapi.io/latest').json()
currencyCodes = [c for c in json_request['rates'].keys()]
currencyCodes.append(json_request['base'])
currencyCodes = sorted(currencyCodes)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html')
def index():

    if request.method == 'POST':
        amount = float(request.form['amount'])
        fromCurrency = request.form['fromCurrency']
        toCurrency = request.form['toCurrency']
        resultString = f"{amount} {fromCurrency} = {conversion(amount,json_request['rates'][fromCurrency],json_request['rates'][toCurrency])} {toCurrency} "
        return render_template('index.html', currencyCodes=currencyCodes, conversionResult=resultString)
    else:
        return render_template('index.html', currencyCodes=currencyCodes)


def conversion(amount, fromCurrency, toCurrency):
    return round(amount * (toCurrency/fromCurrency), 3)


if __name__ == "__main__":
    app.run(debug=True)
