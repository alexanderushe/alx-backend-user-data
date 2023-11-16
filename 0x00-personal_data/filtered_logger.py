#!/usr/bin/env python3
''' function that returns the
log message obfuscated
'''
import logging
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    '''function filters a logline
    '''
    return re.sub(
        fr'({separator.join(fields)}){separator}',
        f'{redaction}{separator}', message)
