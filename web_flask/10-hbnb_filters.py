#!/usr/bin/python3

"""Module that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Display State, City, Amenity"""

    "Fetch and sort States by name (A->Z)"
    obj = storage.all(State).values()
    states = sorted(obj, key=lambda x: x.name)

    "Fetch and sort amenities"
    amenities = storage.all(Amenity).values()
    sorted_amenities = sorted(amenities, key=lambda x: x.name)

    return render_template("10-hbnb_filters.html", states=states,
                           amenities=sorted_amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
