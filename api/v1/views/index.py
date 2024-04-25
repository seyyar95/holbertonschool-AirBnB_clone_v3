#!/usr/bin/python3

"""
This module contains the routes for the index of the API.
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    """Returns a JSON object with the status of the API.

    Returns:
        A JSON object containing the status of the API.

    """
    return jsonify({"status": "OK"})
