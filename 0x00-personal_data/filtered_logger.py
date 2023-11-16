#!/usr/bin/env python3
''' function that returns the
log message obfuscated
'''
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
        record.message = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
