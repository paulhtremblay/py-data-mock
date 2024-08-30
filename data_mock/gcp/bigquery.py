from  data_mock.gcp.table import * 

class TimePartitioning_:

    def __init__(self, type_):
        self.expiration_ms = None
        self.field = None
        self.from_api_repr = None
        self.require_partition_filter = None
        self.to_api_repr = None
        self.type_ = type_

TimePartitioning = TimePartitioning_

class TimePartitioningType:

    DAY=None
    TIME=None

    def __init__(self, *args, **kwargs):
        pass
