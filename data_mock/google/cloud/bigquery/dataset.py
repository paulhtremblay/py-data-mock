class DatasetReference():

    def __init__(self,  project, dataset_id):
        self.project = project
        self.dataset_id = dataset_id

    def table(self, table_id, *args, **kwargs):
        self.table_id = table_id
        return self

class Dataset:
    pass

class DatasetListItem:
    pass
