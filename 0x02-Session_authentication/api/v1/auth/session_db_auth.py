#!/usr/bin/env python3
"""
SessionDBAuth module for authentication with expiration and storage support.
"""
from flask import request
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class extends SessionExpAuth to support database storage.
    """

    def create_session(self, user_id=None) -> str:
        """
        Creates a session ID for a given user ID and stores it in the database.

        Args:
            user_id: The ID of the user to create a session for.

        Returns:
            str: The session ID.
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {'user_id': user_id, 'session_id': session_id}
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID from
        the database.

        Args:
            session_id: The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not
            found or expired.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session from the database, effectively logging
        out the user.

        Args:
            request: The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully deleted,
            False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
