#!/usr/bin/env python3
"""
SessionAuth Module for handling Session authentication
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Authentication class that implement session ID management.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
