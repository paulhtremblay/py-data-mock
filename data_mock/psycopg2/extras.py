_cursor = None
class DictCursorBase():
    pass
class RealDictCursor(DictCursorBase):

    #dummy
    def row_factory(self, *args, **kwargs):
        pass

    #dummy
    def fetchmany(self):
        pass

    #dummy
    def fetchall(self):
        pass

class RealDictRow:
    pass

