#!/usr/bin/env python3
"""
BasicAuth Module for handling basic authentication
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication

        Args:
            authorization_header (str): Authorization header string.

        Returns:
            str: Base64 part of the Authorization header, or None if inValid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str):
        """
        Decode the Base64 part of the Authorization header for Basic

        Args:
            base64_authorization_header (str): Base64 part of the
            Authorization header.

        Returns:
            str: Decoded value of base64_authorization_header
            or None if base64_authorization_header is None or
            base64_authorization_header can't be decoded.
        """

        if base64_authorization_header is None:
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extraction the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            the decode Base64 string containing
            email and password

        Returns:
            tuple: A tuple of (email, password) or (None, None)
            if input is invalid.
        """

        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
