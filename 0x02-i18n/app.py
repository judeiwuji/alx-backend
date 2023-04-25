#!/usr/bin/env python3
"""Module: Flask and Babel App"""
from flask import Flask, render_template, request
import flask
from flask_babel import Babel, format_datetime
from typing import Dict
import pytz
from datetime import datetime


class Config:
    """App configurations"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app=app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def parse_query_str(query: str) -> Dict:
    """parse query string"""
    if query:
        return {d.split("=")[0]: d.split("=")[1]
                for d in query.split("&")}
    return {}


def get_user(id: int):
    """Returns a user with given id"""
    return users.get(id, None)


@app.before_request
def before_request():
    """Executes before each request"""
    query = request.query_string.decode('utf-8')
    queries = parse_query_str(query)
    login_as = queries.get("login_as")
    flask.g.user = None
    if login_as:
        login_as = int(login_as)
        flask.g.user = get_user(login_as)


@babel.localeselector
def get_locale() -> str:
    """returns a locale"""
    query = request.query_string.decode('utf-8')
    queries = parse_query_str(query)
    locale = None
    if queries.get("locale"):
        locale = queries.get("locale")
    elif flask.g.user:
        locale = flask.g.user.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.\
        best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """get timezone"""
    query = request.query_string.decode('utf-8')
    queries = parse_query_str(query)
    timezone = None
    if queries.get("timezone"):
        timezone = queries.get("timezone")
    elif flask.g.user and flask.g.user.get("timezone"):
        timezone = flask.g.user.get("timezone")
    else:
        timezone = app.config['BABEL_DEFAULT_TIMEZONE']

    try:
        pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        timezone = app.config['BABEL_DEFAULT_TIMEZONE']

    return timezone


@app.route('/')
def index():
    """Render index page"""
    return render_template("index.html", user=flask.g.user,
                           current_time=format_datetime(datetime.now()))


if __name__ == "__main__":
    app.run()
