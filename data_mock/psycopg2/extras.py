from collections import OrderedDict

from data_mock.psycopg2.cursor import Cursor
_cursor = None

class DictCursorBase():
    pass
class RealDictCursor(Cursor):

    #dummy
    def row_factory(self, *args, **kwargs):
        pass

    def construct_row(self, row):
        od = OrderedDict()
        for data_obj in row:
            od[data_obj.name] = data_obj.value
        return od


class RealDictRow:
    pass

