from data_mock.gcp.table  import Table

class Dataset:

    def __init__(self, dataset_ref:str):
        self.dataset_id = dataset_ref

    def table(self, table_ref, *args, **kwargs)-> None:
        return Table(table_ref = table_ref)
