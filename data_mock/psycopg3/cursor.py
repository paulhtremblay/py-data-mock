from data_mock.psycopg2.cursor import Cursor as Cursor2

class Cursor(Cursor2):

    def __iter__(self):
        if not hasattr(self, 'data'):
            raise ProgrammingError('no result to fetch')
        if not self.data:
            data = []
        else:
            data = []
        for counter, row in enumerate(data):
            new_row = self.construct_row(row)
            yield new_row
