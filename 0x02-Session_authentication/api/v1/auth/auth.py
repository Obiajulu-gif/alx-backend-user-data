#!/usr/bin/env python3
"""
Authentication Module
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ Auth class template for future authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if the path requires authentication based on excluded paths.

        Args:
            path (str): The request path.
            excluded_paths (List[str]): A list of paths or patterns to exclude
            from authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Normalize path by ensuring it ends with a '/'
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Normalize excluded_path by ensuring it ends with a '/'
            normalized_excluded_path = excluded_path if excluded_path.endswith(
                '/') else excluded_path + '/'
            # Use fnmatch to handle wildcard matching
            if fnmatch.fnmatch(normalized_path, normalized_excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrive the Authorization header from a Flask request Object
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user from a user from
        a Flask request object
        """
        return None
