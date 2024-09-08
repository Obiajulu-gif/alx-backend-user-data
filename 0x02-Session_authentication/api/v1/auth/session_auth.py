#!/usr/bin/env python3
"""
SessionAuth Module for handling Session authentication
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication class that implements session ID management."""

    # Class attribute to store session IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user_id.

        Args:
            user_id (str): The ID of the user to create a session for.

        Returns:
            str: The session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
