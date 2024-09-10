#!/usr/bin/env python3
"""
 a function called filter_datum that returns the log message obfuscated
"""
import os
import re
from typing import List, Tuple
import logging
from mysql.connector.connection import MySQLConnection
import mysql.connector

PII_FIELDS: Tuple[str, ...] = ("name", "email", "ssn", "password", "phone")


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
         filter values in incoming log records using filter_datum
        """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named 'user_data' with a
    RedactingFormatter
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)


def get_db() -> MySQLConnection:
    """
    Connect to the MySQL database using credentials from
    environment variables.

    Returns:
        MySQLConnection: A Connection object to interact
        with the database
    """

    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection
