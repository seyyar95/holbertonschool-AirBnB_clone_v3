#!/usr/bin/python3
"""
This module initializes the blueprint for the API views.

The `app_views` blueprint is created with the name 'app_views' and the URL prefix '/api/v1'.
It imports the views from the `index` module.
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *