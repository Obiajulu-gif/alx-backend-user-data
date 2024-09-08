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

        # Generate a session ID
        session_id = str(uuid.uuid4())

        # Store the session ID with the corresponding user ID
        self.user_id_by_session_id[session_id] = user_id

        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user ID based on the session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID, or None if session_id is invalid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Return the user ID from the dictionary using the session_id
        return self.user_id_by_session_id.get(session_id)
