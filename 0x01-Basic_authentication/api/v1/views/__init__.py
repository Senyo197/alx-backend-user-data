#!/usr/bin/env python3
"""Blueprint configuration for API views.

This module sets up the Blueprint for the API views, ensuring that all routes
are prefixed with /api/v1. It also imports the necessary view modules and
loads user data from a file.
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

User.load_from_file()
