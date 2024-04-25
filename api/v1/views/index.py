#!/usr/bin/python3

"""
This module contains the routes for the index of the API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', strict_slashes=False)
def return_status():
    """Returns a JSON object with the status of the API.

    Returns:
        A JSON object containing the status of the API.

    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def number_of_objects():
    """
    Retrieves the number of each objects by type
    """
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    dictionary = {
            "amenities": amenities,
            "cities": cities,
            "places": places,
            "reviews": reviews,
            "states": states,
            "users": users
            }
    return jsonify(dictionary)
