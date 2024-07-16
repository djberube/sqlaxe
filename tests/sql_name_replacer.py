import unittest
import re
from unittest.mock import patch
from sqlglot import Dialect
from sqlglot.expressions import Table
from sqlaxe.lib.sql_table_name_replacer import SQLTableNameReplacer


class TestSQLTableNameReplacer(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.pretty = True
        self.table_name_regex = r"^table(\d+)$"
        self.table_name_replacement = r"new_table\1"
        self.replacer = SQLTableNameReplacer(
            dialect=self.dialect,
            output_dialect=self.output_dialect,
            pretty=self.pretty,
            table_name_regex=self.table_name_regex,
            table_name_replacement=self.table_name_replacement,
        )

    def test_init(self):
        self.assertEqual(self.replacer.dialect, self.dialect)
        self.assertEqual(self.replacer.output_dialect, self.output_dialect)
        self.assertEqual(self.replacer.pretty, self.pretty)
        self.assertEqual(self.replacer.table_name_regex, self.table_name_regex)
        self.assertEqual(
            self.replacer.table_name_replacement, self.table_name_replacement
        )

    def test_replace_single_table(self):
        sql_content = "SELECT * FROM table1;"
        result = self.replacer.replace(sql_content)
        self.assertEqual(result, "SELECT\n  *\nFROM new_table1;")

    def test_replace_multiple_tables(self):
        sql_content = "SELECT * FROM table1 JOIN table2 ON table1.id = table2.id;"
        result = self.replacer.replace(sql_content)
        self.assertEqual(
            result,
            "SELECT\n  *\nFROM new_table1\nJOIN new_table2\n  ON new_table1.id = new_table2.id;",
        )

    def test_replace_no_match(self):
        sql_content = "SELECT * FROM other_table;"
        result = self.replacer.replace(sql_content)
        self.assertEqual(result, "SELECT\n  *\nFROM other_table;")

    def test_replace_different_output_dialect(self):
        sql_content = "SELECT * FROM table1;"
        self.replacer.output_dialect = "postgres"
        result = self.replacer.replace(sql_content)
        self.assertEqual(result, "SELECT\n  *\nFROM new_table1;")

    def test_replace_no_pretty(self):
        sql_content = "SELECT * FROM table1;"
        self.replacer.pretty = False
        result = self.replacer.replace(sql_content)
        self.assertEqual(result, "SELECT * FROM new_table1;")

    def test_replace_ignore_none_statement(self):
        sql_content = "SELECT * FROM table1; SELECT invalid sql;"
        result = self.replacer.replace(sql_content)
        self.assertEqual(
            result, "SELECT\n  *\nFROM new_table1;\nSELECT\n  invalid AS sql;"
        )


if __name__ == "__main__":
    unittest.main()
