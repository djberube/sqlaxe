import unittest
import re
from unittest.mock import patch
from sqlglot import Dialect
from sqlglot.expressions import Table
import context
from lib.sql_table_name_replacer import SQLTableNameReplacer

class TestSQLTableNameReplacer(unittest.TestCase):

    def setUp(self):
        self.dialect = 'mysql'
        self.output_dialect = 'mysql'
        self.pretty = True
        self.table_name_regex = r'^table(\d+)$'
        self.table_name_replacement = r'new_table\1'
        self.replacer = SQLTableNameReplacer(
            dialect=self.dialect,
            output_dialect=self.output_dialect,
            pretty=self.pretty,
            table_name_regex=self.table_name_regex,
            table_name_replacement=self.table_name_replacement
        )

    def test_init(self):
        self.assertEqual(self.replacer.dialect, self.dialect)
        self.assertEqual(self.replacer.output_dialect, self.output_dialect)
        self.assertEqual(self.replacer.pretty, self.pretty)
        self.assertEqual(self.replacer.table_name_regex, self.table_name_regex)
        self.assertEqual(self.replacer.table_name_replacement, self.table_name_replacement)

    @patch('builtins.print')
    def test_replace_single_table(self, mock_print):
        sql_content = 'SELECT * FROM table1;'
        self.replacer.replace(sql_content)
        mock_print.assert_called_with('SELECT\n  *\nFROM new_table1 /* table1 */;\n')

    @patch('builtins.print')
    def test_replace_multiple_tables(self, mock_print):
        sql_content = 'SELECT * FROM table1 JOIN table2 ON table1.id = table2.id;'
        self.replacer.replace(sql_content)
        mock_print.assert_called_with('SELECT\n  *\nFROM new_table1 /* table1 */\nJOIN new_table2 /* table2 */\n ON new_table1.id = new_table2.id;\n')

    @patch('builtins.print')
    def test_replace_no_match(self, mock_print):
        sql_content = 'SELECT * FROM other_table;'
        self.replacer.replace(sql_content)
        mock_print.assert_called_with('SELECT\n  *\nFROM other_table;\n')

    @patch('builtins.print')
    def test_replace_different_output_dialect(self, mock_print):
        sql_content = 'SELECT * FROM table1;'
        self.replacer.output_dialect = 'postgresql'
        self.replacer.replace(sql_content)
        mock_print.assert_called_with('SELECT\n  *\nFROM "new_table1 /* new_table1 */;\n')

    @patch('builtins.print')
    def test_replace_no_pretty(self, mock_print):
        sql_content = 'SELECT * FROM table1;'
        self.replacer.pretty = False
        self.replacer.replace(sql_content)
        mock_print.assert_called_with('SELECT * FROM new_table1 /* table1 */;\n')

    @patch('builtins.print')
    def test_replace_ignore_none_statement(self, mock_print):
        sql_content = 'SELECT * FROM table1; SELECT invalid sql;'
        self.replacer.replace(sql_content)
        mock_print.assert_called_once_with('SELECT\n  *\nFROM new_table1 /* table1 */;\n')

if __name__ == '__main__':
    unittest.main()
