#!/usr/bin/env python3
''' function that returns the
log message obfuscated
'''

import os
import mysql.connector
import logging
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    '''function filters a logline
    '''
    return re.sub(
        fr'({separator.join(fields)}){separator}',
        f'{redaction}{separator}', message)


def get_logger() -> logging.Logger:
    '''creates a new logger for user data
    '''
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_Handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''creates a connector to a database
    '''
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host = db_host,
        port = 3306,
        user = db_user,
        password = db_pwd,
        database = db_name,
    )
    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''formats a logrecord
        '''
        record.message = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
