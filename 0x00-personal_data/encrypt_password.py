#!/usr/bin/env python3
"""
This module provides functions for password encryption and verification using
bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies if a given password matches its hashed version.

    Args:
        hashed_password (bytes): The hashed password to be verified.
        password (str): The password to check against the hashed password.

    Returns:
        bool: True if the password matches the hashed password, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
