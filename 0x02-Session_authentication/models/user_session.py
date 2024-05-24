#!/usr/bin/env python3
"""
User session module for managing user session data.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class inherits from Base and represents user session data.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance.

        Args:
            *args (list): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
