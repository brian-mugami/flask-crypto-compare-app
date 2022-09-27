import requests
from flask import request, render_template, redirect, url_for, Blueprint, flash
from .forms import SearchForm,AddForm
from .models import Crypto
from website import db

views = Blueprint("views", __name__,template_folder="templates")

@views.route("/", methods=["POST", "GET"])
def index():
    form = AddForm()

    if request.method == "POST":
        name = form.name.data
        existing = Crypto.query.filter_by(name=name).first()

        if existing:
            flash("Crypto already exists, just search for its prices", category="Error")
            return render_template("index.jinja2", form=form)
        else:
            new_crypto = Crypto(name=name, crypto_name=name.lower())
            db.session.add(new_crypto)
            db.session.commit()
            flash("Crypto added ", category="Success")
            return redirect(url_for("views.search"))

    return render_template("index.jinja2", form=form)

@views.route("/search", methods=["POST", "GET"])
def search():
    form = SearchForm()

    if request.method == "POST":
        coin_data = []
        name = form.name.data
        crypto = Crypto.query.filter_by(name=name).first()

        if crypto:
            url = 'https://api.coingecko.com/api/v3/coins/{}?tickers=true&market_data=true&community_data=true&developer_data=true'
            response = requests.get(url.format(crypto.crypto_name)).json()

            coin = {
                "name": crypto.crypto_name,
                "symbol" : response["symbol"],
                "rank" : response["market_cap_rank"],
                "current_price": response["market_data"]["current_price"]["usd"],
                "binance": response["tickers"][0]["converted_last"]["usd"],
                "bibox": response["tickers"][1]["converted_last"]["usd"],
                "digifinex": response["tickers"][2]["converted_last"]["usd"],
                "xt": response["tickers"][3]["converted_last"]["usd"],
                "whitebit": response["tickers"][5]["converted_last"]["usd"],
                "ftx": response["tickers"][6]["converted_last"]["usd"],
                "currency": response["tickers"][8]["converted_last"]["usd"],
                "bitfinex": response["tickers"][9]["converted_last"]["usd"]
            }

            coin_data.append(coin)

            return render_template("search.jinja2", form=form, coin_data=coin_data, crypto=crypto)
        else:
            flash("This coin has not been added", category="Error")

    return render_template("search.jinja2", form=form)


@views.route("/delete/<int:id>")
def delete(id):
    crypto = Crypto.query.get(id)
    db.session.delete(crypto)
    db.session.commit()
    flash("Coin Deleted", category="Success")
    return redirect(url_for("views.search"))






