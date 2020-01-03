import os
from flask import Flask, render_template, request
import requests
from datetime import date, timedelta


from ctfunctions import get_currencyCodes, conversion
import pfunctions
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
    # Plotting default parameters
    default_historic_days = 7
    # API parses this date format: YYYY-MM-DD
    current_date = date.today()
    graph_history = date.today() - timedelta(default_historic_days)
    conversion_form = ConversionForm()

    if request.method == 'POST':
        amount = float(conversion_form.amount.data)
        fromCurrency = conversion_form.fromCurrencyCodeDropdown.data
        toCurrency = conversion_form.toCurrencyCodeDropdown.data

        resultString = f"{amount} {fromCurrency} = {conversion(amount,fromCurrency,toCurrency)} {toCurrency} "

        plotting_graph = pfunctions.parse_plot(
            default_historic_days, fromCurrency, toCurrency)
        return render_template('index.html', form=conversion_form, conversionResult=resultString, plot=plotting_graph)
    else:
        return render_template('index.html', form=conversion_form)


if __name__ == "__main__":
    app.run(debug=True)
