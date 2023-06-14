import os
import sys

from typing import Union, Type

from data_mock.psycopg2.connect import Connect
from data_mock.psycopg3.cursor import Cursor

class Connection(Connect):

    def __init__(self, row_factory = None, *args, **kwargs):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def cursor(self, cursor_factory: Type[Cursor] \
            = Cursor) -> Cursor:
        return cursor_factory(data_provider = self.data_provider)
