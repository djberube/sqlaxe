#!/usr/bin/env python
import unittest
from sqlaxe.lib.sql_list_tables import SQLListTables

class TestSQLListTables(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.list_tables = SQLListTables(dialect=self.dialect)

    def test_extract_tables_select(self):
        sql_content = "SELECT id, name FROM users;"
        self.list_tables.extract_tables(sql_content)
        self.assertEqual(self.list_tables.tables, ['users'])

    def test_extract_tables_create_table(self):
        sql_content = "CREATE TABLE users (id INT, name VARCHAR(255));"
        self.list_tables.extract_tables(sql_content)
        self.assertEqual(self.list_tables.tables, ['users'])

    def test_extract_tables_join(self):
        sql_content = """
        SELECT u.id, p.title
        FROM users u
        JOIN posts p ON u.id = p.user_id;
        """
        self.list_tables.extract_tables(sql_content)
        self.assertEqual(self.list_tables.tables, ['users', 'posts'])

    def test_extract_tables_deduplicates(self):
        sql_content = """
        SELECT id, name FROM users;
        INSERT INTO users (id, name) VALUES (1, 'a');
        SELECT * FROM users WHERE id = 1;
        """
        self.list_tables.extract_tables(sql_content)
        self.assertEqual(self.list_tables.tables, ['users'])

    def test_extract_tables_multiple_statements(self):
        sql_content = """
        SELECT id, name FROM users;
        SELECT title, content FROM posts;
        """
        self.list_tables.extract_tables(sql_content)
        self.assertEqual(self.list_tables.tables, ['users', 'posts'])

    def test_format_csv_output(self):
        sql_content     = "SELECT id, name FROM users;"
        result          = self.list_tables.format(sql_content)
        expected_output = "table_name\r\nusers\r\n"
        self.assertEqual(result, expected_output)

    def test_format_jsonl_output(self):
        self.list_tables = SQLListTables(dialect=self.dialect, output_format='jsonl')
        sql_content = "SELECT id, name FROM users;"
        result = self.list_tables.format(sql_content)
        expected_output = '{"table_name": "users"}'
        self.assertEqual(result, expected_output)

    def test_invalid_output_format(self):
        self.list_tables = SQLListTables(dialect=self.dialect, output_format='invalid')
        sql_content = "SELECT id, name FROM users;"
        with self.assertRaises(ValueError):
            self.list_tables.format(sql_content)

if __name__ == '__main__':
    unittest.main()
