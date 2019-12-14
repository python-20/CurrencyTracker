import os
from flask import Flask, render_template, request
import requests
from ctfunctions import get_currencyCodes, conversion
from wtform_fields import ConversionForm

# import config

app = Flask(__name__)
app.config['DEBUG'] = True

# set up secret key for CSRF
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html')
def index():
    conversion_form = ConversionForm()
    # need to change this block to something like this
    # if request.method == 'POST':
    #    amount = conversion_form.amount.data
    #    fromCurrency = conversion_form.fromCurrencyCodeDropdown.data
    #    toCurrency = conversion_form.toCurrencyCodeDropdown.data
    if request.method == 'POST':
        amount = float(request.form['amount'])
        fromCurrency = request.form['fromCurrency']
        toCurrency = request.form['toCurrency']

        resultString = f"{amount} {fromCurrency} = {conversion(amount,fromCurrency,toCurrency)} {toCurrency} "
        return render_template('index.html', currencyCodes=get_currencyCodes(), conversionResult=resultString)
    else:
        # return render_template('index.html', currencyCodes=get_currencyCodes())
        return render_template('index.html', form=conversion_form)


if __name__ == "__main__":
    app.run(debug=True)
