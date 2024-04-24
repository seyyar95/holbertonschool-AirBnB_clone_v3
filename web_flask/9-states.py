#!/usr/bin/python3
"""Module that starts a Flask web application"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Lists all State objects sorted by name"""
    obj = list(storage.all(State).values())
    states = sorted(obj, key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def cities_of_state(id):
    obj = storage.all(State).values()
    states = sorted(obj, key=lambda x: x.name)
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state, id=id)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
