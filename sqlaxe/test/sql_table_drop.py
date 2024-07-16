import unittest
from unittest.mock import patch
import context
import sqlglot
from sqlglot import Dialect
from sqlglot.expressions import Table, Create
from lib.sql_table_drop import SQLTableDrop


class TestSQLTableDrop(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.table_drop = SQLTableDrop(
            dialect=self.dialect, output_dialect=self.output_dialect
        )

    def test_init(self):
        self.assertEqual(self.table_drop.dialect, self.dialect)
        self.assertEqual(self.table_drop.output_dialect, self.output_dialect)

    def test_drop_table_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result, ["DROP TABLE IF EXISTS mytable", "CREATE TABLE mytable (id INT)"]
        )

    def test_drop_table_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result,
            [
                "DROP TABLE IF EXISTS table1",
                "CREATE TABLE table1 (id INT)",
                "DROP TABLE IF EXISTS table2",
                "CREATE TABLE table2 (id INT)",
            ],
        )

    def test_drop_table_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(result, ["SELECT * FROM mytable"])

    def test_drop_table_different_output_dialect(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        self.table_drop.output_dialect = "postgres"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result, ["DROP TABLE IF EXISTS mytable", "CREATE TABLE mytable (id INT)"]
        )

    def test_format_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_drop.format(sql_content)
        self.assertEqual(
            result, "DROP TABLE IF EXISTS mytable;\nCREATE TABLE mytable (id INT);"
        )

    def test_format_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_drop.format(sql_content)
        self.assertEqual(
            result,
            "DROP TABLE IF EXISTS table1;\nCREATE TABLE table1 (id INT);\nDROP TABLE IF EXISTS table2;\nCREATE TABLE table2 (id INT);",
        )

    def test_format_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_drop.format(sql_content)
        self.assertEqual(result, "SELECT * FROM mytable;")


if __name__ == "__main__":
    unittest.main()
