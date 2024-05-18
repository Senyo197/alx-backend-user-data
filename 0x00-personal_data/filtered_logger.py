#!/usr/bin/env python3
"""
Module for filtering logs.

This module provides functions for filtering logs containing personally
identifiable information (PII). It includes functionality to filter individual
log messages, create a logger for user data, establish a database connection,
and log information about user records from a database table.

Classes:
    RedactingFormatter: A logging formatter class for redacting PII fields in
log messages.
"""

import os
import re
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Formatter class for redacting PII fields from log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize a new RedactingFormatter instance.

        Args:
            fields (List[str]): A list of PII fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log message, redacting PII fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with PII redacted.
        """
        original_message = record.getMessage()
        redacted_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        record.msg = redacted_message
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Filter a log message by redacting specified fields.

    Args:
        fields (List[str]): A list of PII fields to filter.
        redaction (str): The redaction string to use.
        message (str): The log message to filter.
        separator (str): The separator character for the fields.

    Returns:
        str: The filtered log message with PII redacted.
    """
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    replacement = r'\g<field>={}'.format(redaction)
    return re.sub(pattern, replacement, message)


def get_logger() -> logging.Logger:
    """Create and configure a logger for user data.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establish a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection.
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        port=3306,
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME", ""),
    )


def main():
    """Main entry point for logging user data from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, last_login,\
                   user_agent FROM users;")

    logger = get_logger()
    for row in cursor:
        log_message = "name={};email={};phone={};ssn={};password={};last_login\
                       ={};user_agent={};".format(row[0], row[1], row[2],
                                                  row[3], row[4], row[5],
                                                  row[6])
        logger.info(log_message)

    cursor.close()
    db.close()
