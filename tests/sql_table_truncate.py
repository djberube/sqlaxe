import unittest
from unittest.mock import patch
import sqlglot
from sqlglot import Dialect
from sqlglot.expressions import Table, Insert, TruncateTable, Select
from sqlaxe.lib.sql_table_truncate import SQLTableTruncate


class TestSQLTableTruncate(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.table_truncate = SQLTableTruncate(
            dialect=self.dialect, output_dialect=self.output_dialect
        )

    def test_init(self):
        self.assertEqual(self.table_truncate.dialect, self.dialect)
        self.assertEqual(self.table_truncate.output_dialect, self.output_dialect)

    def test_truncate_table_single_insert(self):
        sql_content = "INSERT INTO mytable (id) VALUES (1);"
        result = self.table_truncate.truncate(sql_content)

        self.assertIsInstance(result[0], TruncateTable)
        self.assertEqual(result[0].expressions[0].this.name, "mytable")

        self.assertIsInstance(result[1], Insert)
        self.assertEqual(result[1].this.this.name, "mytable")

    def test_truncate_table_multiple_inserts(self):
        sql_content = (
            "INSERT INTO table1 (id) VALUES (1); INSERT INTO table2 (id) VALUES (2);"
        )
        result = self.table_truncate.truncate(sql_content)
        self.assertIsInstance(result[0], TruncateTable)
        self.assertIsInstance(result[1], Insert)
        self.assertIsInstance(result[2], TruncateTable)
        self.assertIsInstance(result[3], Insert)
        self.assertEqual(result[0].expressions[0].this.this, "table1")
        self.assertEqual(result[1].this.this.name, "table1")
        self.assertEqual(result[2].expressions[0].this.this, "table2")
        self.assertEqual(result[3].this.this.name, "table2")

    def test_truncate_table_no_insert(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_truncate.truncate(sql_content)
        self.assertIsInstance(result[0], Select)
        self.assertEqual(result[0].args["from"].this.name, "mytable")

    def test_truncate_table_different_output_dialect(self):
        sql_content = "INSERT INTO mytable (id) VALUES (1);"
        self.table_truncate.output_dialect = "postgres"
        result = self.table_truncate.truncate(sql_content)
        self.assertIsInstance(result[0], TruncateTable)
        self.assertIsInstance(result[1], Insert)
        self.assertEqual(result[0].expressions[0].this.name, "mytable")
        self.assertEqual(result[1].this.this.name, "mytable")

    def test_format_single_insert(self):
        sql_content = "INSERT INTO mytable (id) VALUES (1);"
        result = self.table_truncate.format(sql_content)
        self.assertEqual(
            result,
            'TRUNCATE TABLE   "mytable";\nINSERT INTO "mytable" (\n  "id"\n)\nVALUES\n  (1);',
        )

    def test_format_multiple_inserts(self):
        sql_content = 'INSERT INTO table1 (id) VALUES (1); INSERT INTO "table2" (id)\n VALUES\n (2);'
        result = self.table_truncate.format(sql_content)
        self.assertEqual(
            result,
            'TRUNCATE TABLE   "table1";\nINSERT INTO "table1" (\n  "id"\n)\nVALUES\n  (1);\nTRUNCATE TABLE   "table2";\nINSERT INTO "table2" (\n  "id"\n)\nVALUES\n  (2);',
        )

    def test_format_no_insert(self):
        sql_content = "SELECT * FROM mytable;"
        result = self.table_truncate.format(sql_content)
        self.assertEqual(result, 'SELECT\n  *\nFROM "mytable";')


if __name__ == "__main__":
    unittest.main()
