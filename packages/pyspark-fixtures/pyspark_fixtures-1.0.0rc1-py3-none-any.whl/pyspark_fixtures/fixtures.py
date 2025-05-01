import re
from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    BooleanType,
    ByteType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
    StructType,
    TimestampType,
)


class SchemaNotFoundError(Exception):
    pass


class PySparkFixtures:
    def __init__(
        self,
        fixtures_file: str,
        spark: SparkSession,
        schemas_fetcher: Callable | None = None,
    ) -> None:
        self._spark = spark
        self._datasets, self._schemas = self._parse_file(fixtures_file, schemas_fetcher)

    @staticmethod
    def _clean_schema_id(schema_id: str) -> str:
        """
        A schema id can be part of a markdown link so it has to be extracted
        """
        clean_schema_id = schema_id.strip()
        potential_md_links = re.search(r"\[([^\]]+)\]\([^\)]+\)", clean_schema_id)
        if potential_md_links:
            clean_schema_id = potential_md_links.group(1).strip()
        return clean_schema_id

    @classmethod
    def _extract_schema_id(cls, lines: list[str]) -> str | None:
        schema_id = None
        for li in lines:
            # If we find a | data has started then there is no schema id
            if re.match(r"^\|", li):
                break
            if re.match(r"^\s*Schema\s*:", li):
                raw_schema_id = li.split(":")[1]
                schema_id = cls._clean_schema_id(raw_schema_id)
                break
        return schema_id

    @classmethod
    def _extract_data_lines(cls, lines: list[str]) -> list[list[str]]:
        return [
            [
                value.replace(r"\|", "|")  # Removing escape character \
                # Spliting by | considering escape char \ and ignoring first and last empty values
                for value in re.split(r"\s*(?<!\\)\|\s*", line.strip())[1:-1]
            ]
            for line in lines
            if re.match(r"^\|", line)  # Lines not starting | are not rows
        ]

    @classmethod
    def _is_markdown_format(cls, data: list[list[str]]) -> bool:
        """
        When is a markdown table the second line has | --- | --- |
        """
        second_line = data[0]
        is_markdown_format = all(
            re.match(r"^\s*[:-]+\s*$", value) for value in second_line
        )
        return is_markdown_format

    @classmethod
    def _parse_dataset(
        cls, lines: list[str]
    ) -> tuple[list[dict], dict | None, str | None]:
        """
        returns:
            - dataset
            - schema
            - schema id if it was defined
        """
        # Extract the schema id if it's defined
        schema_id = cls._extract_schema_id(lines)

        data = cls._extract_data_lines(lines)

        header = data.pop(0)  # The first line is for the columns

        if cls._is_markdown_format(data):
            # If it's in markdown format we have to ignore the line after the header
            # because it's just a markdown format line | --- | --- | --- |
            data.pop(0)

        result_schema = None
        if not schema_id:
            # If no schema id is defined the second linke of data has the schema definition
            schema = data.pop(0)
            result_schema = dict(zip(header, schema))

        result_data = [dict(zip(header, row)) for row in data]

        return (
            result_data,
            result_schema,
            schema_id,
        )

    @classmethod
    def _parse_file(
        cls, fixtures_file: str, schemas_fetcher: Callable | None = None
    ) -> tuple[dict, dict]:
        with open(fixtures_file) as f:
            file_content = f.read()
        datasets = {}
        schemas = {}
        dataset_texts = re.split(
            r"^\s*#*\s*Dataset:\s*", file_content.strip(), flags=re.MULTILINE
        )
        # Skipping anything before the first line with Dataset:
        dataset_texts.pop(0)
        for dataset_raw in dataset_texts:
            lines = dataset_raw.split("\n")
            dataset_name = lines[0].strip()
            # Removing line with the dataset name
            lines.pop(0)
            parsed_dataset, parsed_schema, schema_id = cls._parse_dataset(lines)
            if schema_id and not schemas_fetcher:
                raise SchemaNotFoundError(
                    f"Dataset id '{dataset_name}' has the schema id: '{schema_id}' but not an schema fetcher"
                )
            datasets[dataset_name] = parsed_dataset
            if schema_id and schemas_fetcher:
                schemas[dataset_name] = schemas_fetcher(schema_id)
            elif parsed_schema is not None:
                schemas[dataset_name] = cls._convert_to_struct_type(parsed_schema)
        return datasets, schemas

    @classmethod
    def _convert_to_struct_type(cls, dict_schema: dict) -> StructType:
        fields = []

        for col_name, col_type in dict_schema.items():
            col_type = col_type.lower().strip()
            clean_col_type, num_replacements = re.subn(
                r"\s+not\s+null\s*", "", col_type
            )
            nullable = num_replacements == 0
            fields.append(
                {
                    "name": col_name,
                    "type": clean_col_type,
                    "metadata": {},
                    "nullable": nullable,
                }
            )

        return StructType.fromJson(
            {
                "fields": fields,
                "type": "struct",
            }
        )

    def _cast_col_value(self, col_type: DataType | None, col_value: Any) -> Any:
        if col_value == "<NULL>":
            return None

        if isinstance(col_type, DecimalType):
            return Decimal(col_value)

        if isinstance(col_type, (FloatType, DoubleType)):
            return float(col_value)

        if isinstance(col_type, (ShortType, ByteType, IntegerType, LongType)):
            return int(col_value)

        if isinstance(col_type, DateType):
            return datetime.strptime(col_value, "%Y-%m-%d")

        if isinstance(col_type, TimestampType):
            try:
                return datetime.strptime(col_value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(col_value, "%Y-%m-%d %H:%M:%S.%f")

        if isinstance(col_type, BooleanType):
            if col_value == "false":
                return False
            elif col_value == "true":
                return True
            else:
                return None

        return col_value

    def _cast_dataset(self, dataset: list[dict], schema: StructType) -> list[dict]:
        result = []
        data_types = {field.name: field.dataType for field in schema}

        for row in dataset:
            typed_row = {}
            for col_name, col_value in row.items():
                try:
                    col_type = data_types[col_name]
                except KeyError as ex:
                    raise ValueError(
                        f"Column '{col_name}' not found in the schema"
                    ) from ex
                try:
                    typed_val = self._cast_col_value(col_type, col_value)
                except Exception as ex:
                    raise ValueError(
                        f"Error casting field: '{col_name}', '{col_value}', '{col_type}'"
                    ) from ex
                typed_row[col_name] = typed_val
            result.append(typed_row)

        return result

    def get_schema(self, name: str) -> StructType:
        return self._schemas[name]

    def get_dataset(self, name: str, spark: SparkSession | None = None) -> list[dict]:
        try:
            dataset = self._datasets[name]
        except KeyError as ex:
            raise ValueError(f"Dataset not found '{name}'") from ex
        schema = self.get_schema(name)
        try:
            return self._cast_dataset(dataset, schema)
        except Exception as ex:
            raise ValueError(f"Error casting dataset '{name}'") from ex

    def get_dataframe(self, name: str) -> DataFrame:
        typed_dataset = self.get_dataset(name)
        schema = self.get_schema(name)
        return self._spark.createDataFrame(typed_dataset, schema)
