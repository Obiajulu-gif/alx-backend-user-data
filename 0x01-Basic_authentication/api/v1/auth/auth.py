#!/usr/bin/env python3
"""
Authentication Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class template for future authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required for a given path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Method to retrive the Authorization header from a Flask request Object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user from a user from
        a Flask request object
        """
        return None
