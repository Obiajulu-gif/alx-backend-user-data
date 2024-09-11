#!/usr/bin/env python3
"""
Auth Module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns a salted hash."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
