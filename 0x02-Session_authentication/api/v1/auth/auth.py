#!/usr/bin/env python3
"""
Module for managing API authentication.
"""
import re
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require
            authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path and excluded_paths:
            for excluded_path in excluded_paths:
                excluded_regex = '^{}$'.format(
                    re.escape(excluded_path.rstrip('/')).replace('\\*', '.*')
                    + '/?.*')
                if re.match(excluded_regex, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            str: The value of the Authorization header, or None if not present
        """
        return request.headers.get('Authorization') if request else None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            User: The current user, or None if not authenticated.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieves the session cookie value from the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            str: The value of the session cookie, or None if not present.
        """
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
