from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
import requests
# from rate_dict import currency_dict


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'REALLYSECRETKEY'
csrf = CSRFProtect(app)


def get_rates():
    api_url = 'https://api.apilayer.com/exchangerates_data/latest?base=USD'
    api_key = 'QRvp0kbjyIXQDKIWuUps4MQi7TEMHF4T'

    payload = {}
    headers = {
      "apikey": api_key
    }

    response = requests.request("GET", api_url, headers=headers, data=payload)

    result = response.json()
    return result.get('rates')


currency_dict = get_rates()


class CurrencyForm(FlaskForm):
    money_amount = StringField('Amount of money: ', validators=[DataRequired()])
    from_currency = SelectField('Initial currency', choices=currency_dict.keys())
    to_currency = SelectField('Final currency', choices=currency_dict.keys())
    submit = SubmitField('Exchange')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CurrencyForm()
    data = None
    if form.validate_on_submit():
        money_amount = float(form.money_amount.data)
        from_currency = form.from_currency.data
        to_currency = form.to_currency.data

        final_amount = round(money_amount / currency_dict.get(from_currency) * currency_dict.get(to_currency), 2)

        data = {
            'final_amount': final_amount,
            'money_amount': money_amount,
            'from_currency': from_currency,
            'to_currency': to_currency
        }

    return render_template('index.html', form=form, data=data)


if __name__ == '__main__':
    app.run()
