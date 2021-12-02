from flask import Blueprint, render_template, request
from main import production

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/production")
def production():
    args = request.args
    period = args.get("period")
    return render_template("production.html", period=period, production=production)


@views.route("/capacity")
def capacity():
    args = request.args
    period = args.get("period")
    return render_template("capacity.html", period=period)


@views.route("/procurement")
def procurement():
    args = request.args
    period = args.get("period")
    return render_template("procurement.html", period=period)
