#!/usr/bin/env python3
"""Module: Flask and Babel App"""
from flask import Flask, render_template, request
import flask
from flask_babel import Babel
from typing import Dict


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
    return {d.split("=")[0]: d.split("=")[1]
            for d in query.split("&")}


def get_user(id: int):
    """Returns a user with given id"""
    return users.get(id, None)


@app.before_request
def before_request():
    """Executes before each request"""
    query = request.query_string.decode('utf-8')
    queries = parse_query_str(query)
    login_as = queries.get("login_as")
    if login_as:
        login_as = int(login_as)
        flask.g.user = get_user(login_as)


@babel.localeselector
def get_locale():
    """returns a locale"""
    query = request.query_string.decode('utf-8')
    queries = parse_query_str(query)
    locale = queries.get("locale")
    if locale:
        if locale in app.config['LANGUAGES']:
            return locale
    return request.accept_languages.\
        best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render index page"""
    return render_template("5-index.html", user=flask.g.user)


if __name__ == "__main__":
    app.run()
