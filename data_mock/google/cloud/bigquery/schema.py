class SchemaField:

    def __init__(self, name, field_type, mode = 'Nullable'):
        self.field_type = field_type
        self.name = name
        self.mode = mode

