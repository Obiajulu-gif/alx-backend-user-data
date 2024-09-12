#!/usr/bin/env python3
"""
Auth Module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns a salted hash."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user with email and hashed password.
        if the user already exists, raise a ValueError.

        Args:
            email (str): the user's email
            password (str): the user password

        Returns:
            User: the newly create User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email, hashed_password.decode('utf-8'))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates if login details are correct."""
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Check if the password matches using bcrypt
            if bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password.encode('utf-8')):
                return True
        except NoResultFound:
            # If the user is not found, return False
            return False
        # Return False if password does not match
        return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID and return its string representation."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """Creates a new session for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: Optional[str]) -> Optional[User]:
        """Returns the user associated with the session ID."""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the user's session_id to None.

        Args:
            user_id (int): The ID of the user whose session is being destroyed.

        Returns:
            None
        """
        try:
            # Find the user by their ID
            user = self._db.find_user_by(id=user_id)
            # Update the user's session ID to None
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            # If no user is found, return None
            return None
    

