#!/usr/bin/python3
"""View for State"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    """Retrieves the list of all States objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states', method=['POST'], strict_slashes=False)
def create_state():
    """Creates new state"""
    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    elif "name" not in json.keys():
        abort(400, "Missing name")
    new_state = State(**json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=[
    'GET', 'DELETE', 'PUT'
    ], strict_slashes=False)
def state(state_id):
    """
    For GET method retrieves State object by Id, converts to dict
        and returns it.
    For DELETE method deletes State by Id.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        if request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            json = request.get_json()
            if not json:
                abort(400, description="Not a JSON")
            [setattr(
                state, key, value
                ) for key, value in json.items() if key not in [
                    "id", "created_at", "updated_at"
                    ]]
            storage.save()
            return jsonify(state.to_dict()), 200
        else:
            return jsonify(state.to_dict())
