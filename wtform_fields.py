from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange

from ctfunctions import get_currencyCodes


class ConversionForm(FlaskForm):
    # static string for testing
    # CURRENCY_CODES = [('AUD', 'AUD'), ('CNY', 'CNY'),
    #                  ('EUR', 'EUR'), ('USD', 'USD')]
    CURRENCY_CODES = get_currencyCodes

    amount = StringField('amount_input', validators=[
        InputRequired(message="Amount required"),
        NumberRange(min=0)
    ])
    fromCurrencyCodeDropdown = SelectField(
        'Currency Code', choices=CURRENCY_CODES)
    toCurrencyCodeDropdown = SelectField(
        'Currency Code', choices=CURRENCY_CODES)
    submit = SubmitField()
