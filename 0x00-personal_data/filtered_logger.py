#!/usr/bin/env python3
"""
 a function called filter_datum that returns the log message obfuscated
"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    a function called filter_datum that returns the log message obfuscated:

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
    The function should use a regex to replace occurrences of certain
    field values.
    filter_datum should be less than 5 lines long and use re.sub to perform
    the substitution with a single regex.
    """
    pattern = '|'.join([f"{field}=.*?(?={separator}|$)" for field in fields])
    return re.sub(
        pattern,
        lambda m: m.group(0).split('=')[0] +
        '=' +
        redaction,
        message)
