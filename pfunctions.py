from matplotlib import pyplot as plt
from datetime import date, timedelta
import numpy as np
import requests
import io
import base64

def build_x_historic_array(default_historic_days):
    date_range_array = []
    days = default_historic_days
    for day in range(0, default_historic_days):
        # print(date.today() - timedelta(days))
        days = days - 1
        date_range_array.append(str(date.today() - timedelta(days)))
    return date_range_array

def build_y_array(x_axis_dates_array, quotes, base_currency, selected_currency):
    y_axis_values = []
    for each_day in x_axis_dates_array:
        # if quote query returns None
        if (quotes['rates'].get(each_day)) == None:
            daycounter = 1
            get_rate = quotes['rates'].get(str(date.fromisoformat(each_day) - timedelta(daycounter)))
            # while loop to reduce a day from daycounter if data pull results in NoneType
            while get_rate == None:
                daycounter += 1
                get_rate = quotes['rates'].get(str(date.fromisoformat(each_day) - timedelta(daycounter)))
            # append values to array
            y_axis_values.append(get_rate[selected_currency])
        else:
            # else append values
            y_axis_values.append(quotes['rates'].get(each_day)[selected_currency])
    return y_axis_values

def create_plot(x_axis, y_axis, selected_currency, base_currency, default_historic_days):
    # bytesIO to generate the image "on the fly"
    plot_image = io.BytesIO()

    # Plot
    plt.plot(x_axis, y_axis, color='black', label=f"{selected_currency}")

    # Filling and stuff
    plt.fill_between(x_axis, y_axis, np.min(y_axis), color='mediumturquoise')
    plt.grid()

    # Plot configuration details
    plt.xlabel('Days')
    plt.ylabel(f'Value in {selected_currency}')
    plt.title(f"{base_currency}:{selected_currency} currency history on the last {default_historic_days} days")
    plt.gcf().autofmt_xdate()

    plt.legend()
    plt.tight_layout()

    # FOR DEBUGGING: Show on OS in matplot window
    # plt.show()
    plt.savefig(plot_image, format='png')
    # close
    plt.close()
    # rewind buffer
    plot_image.seek(0)

    plot_url = base64.b64encode(plot_image.getvalue()).decode()
    return 'data:image/png;base64,{}'.format(plot_url)

def parse_plot(default_historic_days, base_currency, selected_currency):
    # Init arrays
    x_axis_dates_array = None
    y_axis = None

    # API parses this date format: YYYY-MM-DD
    current_date = date.today()
    graph_history = date.today() - timedelta(default_historic_days)
    
    # Build X array with dates
    x_axis_dates_array = build_x_historic_array(default_historic_days)

    # Get the rates: https://api.exchangeratesapi.io/history?start_at=2018-01-01&end_at=2018-09-01
    parameters = {'start_at': graph_history, 'symbols': selected_currency, 'end_at': current_date, 'base':base_currency}

    json_request_historic = requests.get(
        'https://api.exchangeratesapi.io/history', params=parameters).json()

    quotes = requests.get('https://api.exchangeratesapi.io/history', params=parameters).json()

    # Build Y array based on the dates from X array
    y_axis = build_y_array(x_axis_dates_array, quotes, base_currency, selected_currency)

    print(f'Debug: from_currency:{base_currency}, to_currency:{selected_currency}')
    print(f'Debug: x_axis:{x_axis_dates_array}, y_axis:{y_axis}')

    # Plot Generation
    image_plot = create_plot(x_axis_dates_array, y_axis, selected_currency, base_currency, default_historic_days)
    return image_plot


# # # Default variables to test
# default_historic_days = 10
# selected_currency = 'USD'
# base_currency = 'EUR'


