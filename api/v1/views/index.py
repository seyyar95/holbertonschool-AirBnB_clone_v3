from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    """Returns a JSON object"""
    return jsonify({"status": "OK"})
