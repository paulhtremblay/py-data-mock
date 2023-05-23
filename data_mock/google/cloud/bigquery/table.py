from . import schema
from . import exceptions as _exceptions

class Table:

    def _get_table_info(self, table_ref):
        if hasattr(table_ref, 'dataset_ref'):
            self.project = table_ref.dataset_ref.project
            self.dataset_id = table_ref.dataset_ref.dataset_id
            self.table_id = table_ref.table_id
        elif not isinstance(table_ref, str):
            raise _exceptions.InvalidMockData('table id must be <table_ref> or <str>')
        else:
            fields = table_ref.split('.')
            if len(fields) != 3:
                raise _exceptions.InvalidData('table id must be in format "project_id.dataset_id.table_id"')
            self.project = fields[0]
            self.dataset_id= fields[1]
            table_id = fields[2]
            self.table_id = f'{self.project}.{self.dataset_id}.{table_id}'

    def __init__(self, table_ref, schema = None):
        self._get_table_info(table_ref)
        self.schema = schema


class TimePartitioning:

    def __init__(self, type_=None, field=None, 
            expiration_ms=None, require_partition_filter=None):
        self.field = field


class TableReference:

    def __init__(self, dataset_ref, table_id):
        self.dataset_ref = dataset_ref
        self.table_id = table_id


class Row():

    def __init__(self, row):
        self.__info = {}
        l = []
        for i in row:
            self.__info[i.name] = i.value
            l.append(i.value)
        self.__values = tuple(l)
        self.row = row

    def get(self, *args, **kwargs):
        if args:
            return self.__info.get(args[0])
        return self.__info.get(kwargs['key'])

    def items(self, *args, **kwargs):
        for i in self.row:
            yield i.name, i.value

    def values(self, *args, **kwargs):
        return self.__values

    def keys(self, *args, **kwargs):
        return self.__info.keys()

class RowIterator:

    def __init__(self, data, m):
        if data == None:
            def none_generator():
                return
                yield
            self.__data = none_generator()
            self.total_rows = 0
        else:
            self.__data = data
            self.total_rows = m.get('total_rows')
            self.schema = m.get('schema')

    def __iter__(self):
        return self

    def __next__(self):
        v = next(self.__data)
        if not v:
            raise StopIteration
        else:
            return Row(row = v)

    def result(self):
        return self


class TimePartitioningType:
    """Specifies the type of time partitioning to perform."""

    DAY = "DAY"
    """str: Generates one partition per day."""

    HOUR = "HOUR"
    """str: Generates one partition per hour."""

    MONTH = "MONTH"
    """str: Generates one partition per month."""

    YEAR = "YEAR"
    """str: Generates one partition per year."""

class TableListItem(Table):

    def __init__(self):
        self.tables = []
        super().__init__()
