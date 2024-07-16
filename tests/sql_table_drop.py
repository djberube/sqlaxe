import unittest
from unittest.mock import patch
import sqlglot
from sqlglot import Dialect
from sqlglot.expressions import Table, Create
from sqlaxe.lib.sql_table_drop import SQLTableDrop


class TestSQLTableDrop(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.table_drop = SQLTableDrop(
            dialect=self.dialect, output_dialect=self.output_dialect
        )

    def test_drop_table_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result,
            ["DROP TABLE IF EXISTS mytable CASCADE", "CREATE TABLE mytable (id INT)"],
        )

    def test_drop_table_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result,
            [
                "DROP TABLE IF EXISTS table1 CASCADE",
                "CREATE TABLE table1 (id INT)",
                "DROP TABLE IF EXISTS table2 CASCADE",
                "CREATE TABLE table2 (id INT)",
            ],
        )

    def test_drop_table_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(result, ["SELECT * FROM mytable"])

    def test_drop_table_different_output_dialect(self):
        self.table_drop = SQLTableDrop(output_dialect="postgres")
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_drop.drop_table(sql_content)
        self.assertEqual(
            result,
            ["DROP TABLE IF EXISTS mytable CASCADE", "CREATE TABLE mytable (id INT)"],
        )

    def test_format_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_drop.format(sql_content)
        self.assertEqual(
            result,
            "DROP TABLE IF EXISTS mytable CASCADE;\nCREATE TABLE mytable (id INT);",
        )

    def test_format_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_drop.format(sql_content)
        self.assertEqual(
            result,
            "DROP TABLE IF EXISTS table1 CASCADE;\nCREATE TABLE table1 (id INT);\nDROP TABLE IF EXISTS table2 CASCADE;\nCREATE TABLE table2 (id INT);",
        )

    def test_format_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_drop.format(sql_content)
        self.assertEqual(result, "SELECT * FROM mytable;")


if __name__ == "__main__":
    unittest.main()
