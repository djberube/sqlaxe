import unittest
import os
import shutil
from sqlglot import Dialect
from sqlglot.expressions import Table
from sqlglot.tokens import Token

import context
import sqlglot
from lib.sql_grep import SQLGrep

class TestSQLGrep(unittest.TestCase):

    def setUp(self):
        self.sql_file = 'test.sql'
        self.dialect = 'mysql'
        self.output_dialect = 'mysql'
        self.grep = SQLGrep(
            pattern='table1',
            dialect=self.dialect,
            output_dialect=self.output_dialect,
            invert=False
        )

    def tearDown(self):
        return True

    def test_init(self):
        self.assertEqual(self.grep.dialect, self.dialect)
        self.assertEqual(self.grep.output_dialect, self.output_dialect)

    def test_grep(self):
        test_sql = 'SELECT * from table1; SELECT * FROM table2; SELECT \n\t\tid FROM table1;'
        pattern = 'SELECT \* FROM table1'

        content = self.grep.format(test_sql)


        self.assertIn('SELECT\n  *\nFROM "table1";\n', content)
        self.assertIn('SELECT\n  "id"\nFROM "table1";', content)
        self.assertNotIn('SELECT\n  *\nFROM "table2";\n', content)

if __name__ == '__main__':
    unittest.main()
