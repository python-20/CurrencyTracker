from flask import Flask, render_template, request
import requests
from ctfunctions import get_currencyCodes, conversion

# import config

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html')
def index():

    if request.method == 'POST':
        amount = float(request.form['amount'])
        fromCurrency = request.form['fromCurrency']
        toCurrency = request.form['toCurrency']

        resultString = f"{amount} {fromCurrency} = {conversion(amount,fromCurrency,toCurrency)} {toCurrency} "
        return render_template('index.html', currencyCodes=get_currencyCodes(), conversionResult=resultString)
    else:
        return render_template('index.html', currencyCodes=get_currencyCodes())


if __name__ == "__main__":
    app.run(debug=True)
