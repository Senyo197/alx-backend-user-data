#!/usr/bin/env python3
"""Module to manage API authentication."""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require
            authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is not None and excluded_paths is not None:
            for excluded_path in excluded_paths:
                excluded_regex = '^{}$'.format(re.escape(
                    excluded_path.rstrip('/')).replace('\\*', '.*') + '/?.*')
                if re.match(excluded_regex, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            str: The value of the Authorization header, or None if not present.
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
