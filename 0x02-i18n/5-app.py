#!/usr/bin/env python3
"""Module: Flask and Babel App"""
from flask import Flask, render_template, request
import flask
from flask_babel import Babel


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


def get_user(id: int):
    """Returns a user with given id"""
    return users.get(id, None)


@app.before_request
def before_request():
    """Executes before each request"""
    query = request.query_string.decode('utf-8')
    queries = query.split("=")
    login_as = None
    if query and "login_as" in query:
        login_as = int(queries[1])
    flask.g.user = get_user(login_as)


@babel.localeselector
def get_locale():
    """returns a locale"""
    lang = request.query_string.decode("utf-8")
    if lang and "locale=" in lang:
        lang = lang.split("=")
        selected = lang[1]
        if selected in app.config['LANGUAGES']:
            return selected
    return request.accept_languages.\
        best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render index page"""
    return render_template("5-index.html", user=flask.g.user)


if __name__ == "__main__":
    app.run()
