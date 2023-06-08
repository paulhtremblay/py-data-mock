from typing import Any, Dict, Iterable, Union, Optional
import enum

class SchemaField(object):

    def __init__(
        self,
        name: str,
        field_type: str,
        mode: str = "NULLABLE",
        default_value_expression: Optional[str] = None,
        description: str = '',
        fields: Iterable["SchemaField"] = (),
        policy_tags: Optional[str] = None,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        self.mode = mode
        self.field_type = field_type
        self.name = name
        self.default_value_expression = default_value_expression
        self.description = description
        self.fields = fields
