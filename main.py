import requests
import csv
import json
from flask import Flask, render_template, request, url_for

def get_exchangerates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    return response.json()


def convert_to_csv():
    data = get_exchangerates()
    with open('my.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        for table in data:
            for rate in table["rates"]:
                writer.writerow(rate.values())




def main():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def render_page():
        exchangerates = get_exchangerates()[0]
        rates = exchangerates['rates']
        codes = [rate['code'] for rate in rates]
        to_buy, value = 0, 0
        selected = ""


        if request.method == "POST":
            form = request.form
            if "buy" in form.keys():
                bid = [rate['bid'] for rate in rates if rate['code'] == form['currency']][0]
                selected = form['currency']
                value  = float(bid) * float(form["buy"])
                to_buy = float(form["buy"])

        return render_template("index.html", code_list = codes, selected = selected, to_buy = to_buy, val = value)

    return app

if __name__ == "__main__":
    # convert_to_csv()
    app = main()
    app.run(debug=True)


