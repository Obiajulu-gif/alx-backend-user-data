#!/usr/bin/env python3
"""
hash_password function that expects one string
argument name password and returns a salted,
hashed password, which is a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with automatic salting.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a provided password against a hashed password using bcrypt.
    
    Args: 
        hashed_password (bytes): hashed password
        password (str): plain text password to validate
        
    Returns:
        bool: True if the password matches the hashed password, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
