#!/usr/bin/env python3
"""
DB module to interact with the user database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id',
                'reset_token']


class DB:
    """DB class for handling database operations."""

    def __init__(self) -> None:
        """Initialize a new DB instance with SQLite database."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # Drop and create all tables
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the database and returns the User object.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created user object.
        """
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)
        # Add the user to the session
        self._session.add(new_user)
        # Commit the changes to the database
        self._session.commit()
        # Return the newly created user object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments.

        Args:
            kwargs: Arbitrary keyword arguments (e.g., email='test@test.com')

        Returns:
            User: The first matching user.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If an invalid query argument is provided.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound
