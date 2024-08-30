from typing import Union, Optional, Sequence, Type, TypeVar, Optional, List, Dict, Tuple
class RowIterator:

    def __init__(self, data:Union[List[List[tuple]], None] = None, 
            meta:Union[dict, None] = None):
        if data == None:
            def none_generator():
                return
                yield
            self.__data = none_generator()
            self.total_rows = 0
        else:
            def my_generator():
                for i in data:
                    yield i
            self.__data = my_generator()
            self.total_rows = meta.get('total_rows')
            self.schema = meta.get('schema')

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

class Row():

    def __init__(self, row:List[Tuple]):
        self.__info = {}
        l = []
        for i in row:
            self.__info[i[0]] = i[1]
            l.append(i[1])
            self.__dict__[i[0]] = i[1]
        self.__values = tuple(l)
        self.row = row

    def get(self, *args, **kwargs):
        if args:
            return self.__info.get(args[0])
        return self.__info.get(kwargs['key'])

    def items(self, *args, **kwargs):
        for i in self.row:
            yield i[0], i[1]

    def values(self, *args, **kwargs):
        return self.__values

    def keys(self, *args, **kwargs):
        return self.__info.keys()

def _set_defaults_for_table(kwargs):

    d = {}
    default = [
    'clone_definition',
    'clustering_fields',
    'created',
    'dataset_id',
    'description',
    'encryption_configuration',
    'etag',
    'expires',
    'external_data_configuration',
    'friendly_name',
    'from_api_repr',
    'from_string',
    'full_table_id',
    'labels',
    'location',
    'modified',
    'mview_enable_refresh',
    'mview_last_refresh_time',
    'mview_query',
    'mview_refresh_interval',
    'num_bytes',
    'num_rows',
    'partition_expiration',
    'partitioning_type',
    'path',
    'project',
    'range_partitioning',
    'reference',
    'require_partition_filter',
    'schema',
    'self_link',
    'snapshot_definition',
    'streaming_buffer',
    'table_constraints',
    'table_id',
    'table_type',
    'time_partitioning',
    'to_api_repr',
    'to_bqstorage',
    'view_query',
    'view_use_legacy_sql',
    ]
    for i in default:
        d[i] = kwargs.get(i)
    return d

class Table:

    def __init__(self, table_ref:Union[str, None] = None, *args, **kwargs):
        self.project = None
        d = _set_defaults_for_table(kwargs)
        for key in d.keys():
            self.__dict__[key] = d[key]
        if hasattr(table_ref, 'table_id'):
            self.table_id = table_ref.table_id
        else:
            self.table_id = table_ref

class TableReference:
    pass

class TableListItem:
    pass

