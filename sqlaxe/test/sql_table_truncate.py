import unittest
from unittest.mock import patch
import context
import sqlglot
from sqlglot import Dialect
from sqlglot.expressions import Table, Create
from lib.sql_table_truncate import SQLTableTruncate

class TestSQLTableTruncate(unittest.TestCase):

    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.table_truncate = SQLTableTruncate(
            dialect=self.dialect,
            output_dialect=self.output_dialect
        )

    def test_init(self):
        self.assertEqual(self.table_truncate.dialect, self.dialect)
        self.assertEqual(self.table_truncate.output_dialect, self.output_dialect)

    def test_truncate_table_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_truncate.truncate(sql_content)
        self.assertEqual(result, ["TRUNCATE TABLE mytable", "CREATE TABLE mytable (id INT)"])

    def test_truncate_table_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_truncate.truncate(sql_content)
        self.assertEqual(result, [
            "TRUNCATE TABLE table1",
            "CREATE TABLE table1 (id INT)",
            "TRUNCATE TABLE table2",
            "CREATE TABLE table2 (id INT)"
        ])

    def test_truncate_table_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_truncate.truncate(sql_content)
        self.assertEqual(result, ["SELECT * FROM mytable"])

    def test_truncate_table_different_output_dialect(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        self.table_truncate.output_dialect = "postgres"
        result = self.table_truncate.truncate(sql_content)
        self.assertEqual(result, ['TRUNCATE TABLE mytable', 'CREATE TABLE mytable (id INT)'])

    def test_format_single_create_table(self):
        sql_content = "CREATE TABLE mytable (id INT);"
        result = self.table_truncate.format(sql_content)
        self.assertEqual(result, "TRUNCATE TABLE mytable;\nCREATE TABLE mytable (id INT);")

    def test_format_multiple_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT); CREATE TABLE table2 (id INT);"
        result = self.table_truncate.format(sql_content)
        self.assertEqual(result, "TRUNCATE TABLE table1;\nCREATE TABLE table1 (id INT);\nTRUNCATE TABLE table2;\nCREATE TABLE table2 (id INT);")

    def test_format_no_create_table(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_truncate.format(sql_content)
        self.assertEqual(result, "SELECT * FROM mytable;")


if __name__ == '__main__':
    unittest.main()
