from flask import Flask, render_template
import requests

# import config

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    request = requests.get('https://api.exchangeratesapi.io/latest').json()

    # show json string in log
    app.logger.info(request)

    # test block
    rates = {
        'base': request['base'],
        'date': request['date'],
        'AUD': request['rates']['AUD'],
        'USD': request['rates']['USD']
    }

    app.logger.info(rates)
    # end test block

    # test conversion function
    fromCurrency = 'USD'
    toCurrency = 'AUD'
    app.logger.info(
        f"{fromCurrency} to {toCurrency} = {conversion(1,rates[fromCurrency],rates[toCurrency])}")

    return render_template('index.html', rates = request['rates'])


def conversion(amount, fromCurrency, toCurrency):
    return round(amount * fromCurrency/toCurrency, 3)



if __name__ == "__main__":
    app.run(debug=True)
