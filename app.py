from flask import Flask, render_template
import requests

# import config

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    request = requests.get('https://api.exchangeratesapi.io/latest').json()
    app.logger.info(request)

    rates = {
        'base': request['base'],
        'date': request['date'],
        'AUD': request['rates']['AUD']
    }

    app.logger.info(rates)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
