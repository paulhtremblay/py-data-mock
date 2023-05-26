from typing import Any, Dict, Iterable, Union
import enum

class SchemaField(object):

    """
    def __init__(self, name, field_type, mode = 'Nullable',
                 fields = None):
        self.field_type = field_type
        self.name = name
        self.mode = mode
    """

    def __init__(
        self,
        name: str,
        field_type: str,
        mode: str = "NULLABLE",
        default_value_expression: str = None,
        description: str = '',
        fields: Iterable["SchemaField"] = (),
        policy_tags: str = None,
        precision: int = None,
        scale: int = None,
        max_length: int = None,
    ):
        self.mode = mode
        self.field_type = field_type
        self.name = name
        self.default_value_expression = default_value_expression
        self.description = description
        self.fields = fields
