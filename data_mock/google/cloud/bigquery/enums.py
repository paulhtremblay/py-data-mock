class SourceFormat:
    """The format of the data files. The default value is :attr:`CSV`.

    Note that the set of allowed values for loading data is different
    than the set used for external data sources (see
    :class:`~google.cloud.bigquery.external_config.ExternalSourceFormat`).
    """

    CSV = "CSV"
    """Specifies CSV format."""

    DATASTORE_BACKUP = "DATASTORE_BACKUP"
    """Specifies datastore backup format"""

    NEWLINE_DELIMITED_JSON = "NEWLINE_DELIMITED_JSON"
    """Specifies newline delimited JSON format."""

    AVRO = "AVRO"
    """Specifies Avro format."""

    PARQUET = "PARQUET"
    """Specifies Parquet format."""

    ORC = "ORC"
    """Specifies Orc format."""

class WriteDisposition:
    """Specifies the action that occurs if destination table already exists.

    The default value is :attr:`WRITE_APPEND`.

    Each action is atomic and only occurs if BigQuery is able to complete
    the job successfully. Creation, truncation and append actions occur as one
    atomic update upon job completion.
    """

    WRITE_APPEND = "WRITE_APPEND"
    """If the table already exists, BigQuery appends the data to the table."""

    WRITE_TRUNCATE = "WRITE_TRUNCATE"
    """If the table already exists, BigQuery overwrites the table data."""

    WRITE_EMPTY = "WRITE_EMPTY"
    """If the table already exists and contains data, a 'duplicate' error is
    returned in the job result."""

