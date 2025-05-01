import logging
import os
from datetime import datetime
from decimal import Decimal

import pytest
from pyspark.sql.types import (
    IntegerType,
    DateType,
    DecimalType,
    StringType,
    StructField,
    StructType,
)

from pyspark_fixtures.fixtures import (
    PySparkFixtures,
    SchemaNotFoundError,
)

from pyspark_fixtures.helpers import (
    compare_lists,
    compare_dfs_schemas,
    get_spark_session,
    get_table_schema,
)

logger = logging.getLogger()


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_SPARK_WAREHOUSE_DIR = os.path.join(TEST_DIR, "pytest-spark-warehouse")


class TestPySparkFixtures:
    _spark = get_spark_session(TEST_SPARK_WAREHOUSE_DIR)

    FILE_FIXTURES_PATH = f"{TEST_DIR}/testing_data_documentation.md"

    @staticmethod
    def schemas_fetcher(dataset_name: str):
        db_name, table_name, *_ = dataset_name.split(".")
        return get_table_schema(db_name, table_name, base_path=f"{TEST_DIR}/schemas")

    def test__test_fixtures_class(self):
        fixtures = PySparkFixtures(
            self.FILE_FIXTURES_PATH, self._spark, self.schemas_fetcher
        )
        expected_datasets = {
            "ds_1": [
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 11, 1, 0, 0),
                    "some_value": Decimal("2.000"),
                    "some_other_value": Decimal("20.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 9, 1, 0, 0),
                    "some_value": Decimal("0.000"),
                    "some_other_value": Decimal("100.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 8, 1, 0, 0),
                    "some_value": Decimal("4.000"),
                    "some_other_value": Decimal("70.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 7, 1, 0, 0),
                    "some_value": Decimal("5.000"),
                    "some_other_value": Decimal("53.500"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 5, 1, 0, 0),
                    "some_value": Decimal("7.550"),
                    "some_other_value": Decimal("353.000"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 4, 1, 0, 0),
                    "some_value": Decimal("41.200"),
                    "some_other_value": Decimal("1.300"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyyyyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 3, 1, 0, 0),
                    "some_value": Decimal("1100.680"),
                    "some_other_value": Decimal("8001.000"),
                },
            ],
            "ds_2": [
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 11, 1, 0, 0),
                    "some_value": Decimal("4.000"),
                    "some_other_value": Decimal("40.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 9, 1, 0, 0),
                    "some_value": Decimal("20.000"),
                    "some_other_value": Decimal("300.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxxxxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 8, 1, 0, 0),
                    "some_value": Decimal("6.000"),
                    "some_other_value": Decimal("90.000"),
                },
                {
                    "col1": "cat1",
                    "col2": "xxx|xxx33",
                    "col3": "0002",
                    "col4": "A1",
                    "some_date": datetime(2025, 7, 1, 0, 0),
                    "some_value": Decimal("7.000"),
                    "some_other_value": Decimal("73.500"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyy|yyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 5, 1, 0, 0),
                    "some_value": Decimal("27.550"),
                    "some_other_value": Decimal("553.000"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyy|yyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 4, 1, 0, 0),
                    "some_value": Decimal("61.200"),
                    "some_other_value": Decimal("201.300"),
                },
                {
                    "col1": "cat2",
                    "col2": "yyy|yyyjp",
                    "col3": "0004",
                    "col4": "B2",
                    "some_date": datetime(2025, 3, 1, 0, 0),
                    "some_value": Decimal("2200.680"),
                    "some_other_value": Decimal("10001.000"),
                },
            ],
        }

        assert expected_datasets["ds_1"] == fixtures.get_dataset("ds_1")

        assert expected_datasets["ds_1"] == fixtures.get_dataset("dataset_md_format")

        assert expected_datasets["ds_2"] == fixtures.get_dataset("ds_2")

        result_df = fixtures.get_dataframe("ds_2")

        expected_schema = StructType(
            [
                StructField("col1", StringType(), True),
                StructField("col2", StringType(), True),
                StructField("col3", StringType(), True),
                StructField("col4", StringType(), True),
                StructField("some_date", DateType(), True),
                StructField("some_value", DecimalType(38, 8), True),
                StructField("some_other_value", DecimalType(38, 8), False),
            ]
        )
        compare_dfs_schemas(result_df.schema, expected_schema, check_nullability=True)

    @pytest.mark.parametrize(
        "raw_schema_id, expected_result",
        [
            (
                "  some_db.some_table   ",
                "some_db.some_table",
            ),
            (
                r"[test_db.test_table](../schemas/test_db/test_table.json)",
                "test_db.test_table",
            ),
            (
                r"[  other_schema.other_table   ](../schemas/test_db/test_table.json)",
                "other_schema.other_table",
            ),
        ],
    )
    def test__test_fixtures_class__clean_raw_schema_id(
        self, raw_schema_id, expected_result
    ):
        assert PySparkFixtures._clean_schema_id(raw_schema_id) == expected_result

    def test__test_fixtures_class_no_schema(self):
        with pytest.raises(SchemaNotFoundError) as ex:
            PySparkFixtures(self.FILE_FIXTURES_PATH, self._spark)
        assert (
            str(ex.value)
            == "Dataset id 'ds_schema_fetcher_1' has the schema id: 'test_db.test_table' but not an schema fetcher"
        )

    def test__test_fixtures_class_schema_fetcher(self):
        fixtures = PySparkFixtures(
            self.FILE_FIXTURES_PATH, self._spark, self.schemas_fetcher
        )
        result_df1 = fixtures.get_dataframe("ds_schema_fetcher_1")

        expected_output = [
            {"test_col1": "aaa", "test_col2": 1},
            {"test_col1": "bbb", "test_col2": 2},
            {"test_col1": "ccc", "test_col2": 3},
        ]
        compare_lists(
            [r.asDict() for r in sorted(result_df1.collect())], expected_output
        )
        result_df2 = fixtures.get_dataframe("ds_schema_fetcher_2")
        compare_lists(
            [r.asDict() for r in sorted(result_df2.collect())], expected_output
        )

    def test_compare_dfs_schemas_matching_without_nullability(self):
        schema1 = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), False),
            ]
        )
        schema2 = StructType(
            [
                StructField("name", StringType(), False),  # nullability ignored
                StructField("age", IntegerType(), True),
            ]
        )
        compare_dfs_schemas(schema1, schema2, check_nullability=False)

        def test_compare_dfs_schemas_matching_with_nullability(self):
            schema1 = StructType(
                [
                    StructField("name", StringType(), True),
                    StructField("age", IntegerType(), False),
                ]
            )
            schema2 = StructType(
                [
                    StructField("name", StringType(), True),
                    StructField("age", IntegerType(), False),
                ]
            )
            compare_dfs_schemas(schema1, schema2, check_nullability=True)

        def test_compare_dfs_schemas_mismatched_column_name(self):
            schema1 = StructType(
                [
                    StructField("name", StringType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("full_name", StringType(), True),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2)

        def test_compare_dfs_schemas_mismatched_data_type(self):
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", StringType(), True),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2)

        def test_compare_dfs_schemas_mismatched_nullability_with_check(self):
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", IntegerType(), False),
                ]
            )
            with pytest.raises(AssertionError, match="Schemas mismatch found"):
                compare_dfs_schemas(schema1, schema2, check_nullability=True)

        def test_compare_dfs_schemas_ignore_nullability_difference(self):
            schema1 = StructType(
                [
                    StructField("age", IntegerType(), True),
                ]
            )
            schema2 = StructType(
                [
                    StructField("age", IntegerType(), False),
                ]
            )
            compare_dfs_schemas(schema1, schema2, check_nullability=False)

    def test_compare_dfs_schemas_column_order_matters(self):
        schema1 = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True),
            ]
        )
        schema2 = StructType(
            [
                StructField("age", IntegerType(), True),
                StructField("name", StringType(), True),
            ]
        )
        with pytest.raises(AssertionError):
            compare_dfs_schemas(schema1, schema2)
