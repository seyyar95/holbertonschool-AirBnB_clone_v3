#!/usr/bin/python3
"""Module that starts a Flask web application"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_text(text):
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python/", strict_slashes=False, defaults={"text": "is_cool"})
@app.route("/python/<text>", strict_slashes=False)
def python_text(text):
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route("/number/<int:n>", strict_slashes=True)
def display_number(n):
    return f'{n} is a number'


@app.route("/number_template/<int:n>", strict_slashes=True)
def display_html(n):
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
