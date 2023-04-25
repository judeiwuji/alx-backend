#!/usr/bin/env python3
"""Module: Flask and Babel App"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """App configurations"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app=app)


@babel.localeselector
def get_locale():
    """returns a locale"""
    return request.accept_languages.\
        best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render index page"""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run()
