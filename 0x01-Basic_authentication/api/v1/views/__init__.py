#!/usr/bin/env python3
"""Blueprint configuration for API views.

This module sets up the Blueprint for the API views, ensuring that all routes
are prefixed with /api/v1. It also imports the necessary view modules and
loads user data from a file.
"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *


# Create a Blueprint for the API views with a URL prefix of /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Load user data from file
User.load_from_file()
