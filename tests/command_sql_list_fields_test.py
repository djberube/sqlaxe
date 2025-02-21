#!/usr/bin/env python
import unittest
from sqlaxe.lib.sql_list_fields import SQLListFields

class TestSQLListFields(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.list_fields = SQLListFields(dialect=self.dialect)

    def test_extract_fields_select(self):
        sql_content = "SELECT id, name FROM users;"
        self.list_fields.extract_fields(sql_content)
        expected_fields = [
            {'field_name': 'id', 'table_name': 'users'},
            {'field_name': 'name', 'table_name': 'users'}
        ]
        self.assertEqual(self.list_fields.fields, expected_fields)

    def test_extract_fields_with_table_name(self):
        sql_content = "SELECT users.id, users.name FROM users;"
        self.list_fields.extract_fields(sql_content)
        expected_fields = [
            {'field_name': 'id', 'table_name': 'users'},
            {'field_name': 'name', 'table_name': 'users'}
        ]
        self.assertEqual(self.list_fields.fields, expected_fields)


    def test_extract_fields_create_table(self):
        sql_content = "CREATE TABLE users (id INT, name VARCHAR(255));"

        self.list_fields.extract_fields(sql_content)

        expected_fields = [
            {'field_name': 'id', 'table_name': 'users'},
            {'field_name': 'name', 'table_name': 'users'}
        ]

        self.assertEqual(self.list_fields.fields, expected_fields)

    def test_format_csv_output(self):
        sql_content     = "SELECT id, name FROM users;"
        result          = self.list_fields.format(sql_content)
        expected_output = "field_name,table_name\r\nid,users\r\nname,users\r\n"
        self.assertEqual(result, expected_output)

    def test_format_jsonl_output(self):
        self.list_fields = SQLListFields(dialect=self.dialect, output_format='jsonl')
        sql_content = "SELECT id, name FROM users;"
        result = self.list_fields.format(sql_content)
        expected_output = '{"field_name": "id", "table_name": "users"}\n{"field_name": "name", "table_name": "users"}'
        self.assertEqual(result, expected_output)

    def test_invalid_output_format(self):
        self.list_fields = SQLListFields(dialect=self.dialect, output_format='invalid')
        sql_content = "SELECT id, name FROM users;"
        with self.assertRaises(ValueError):
            self.list_fields.format(sql_content)

    def test_complex_query(self):
        sql_content = """
        SELECT 
            u.id as user_id,
            u.name,
            p.title as post_title
        FROM users u
        JOIN posts p ON u.id = p.user_id;
        """

        self.list_fields.extract_fields(sql_content)

        expected_fields = [
            {'field_name': 'id', 'table_name': 'users' },
            {'field_name': 'name', 'table_name': 'users'},
            {'field_name': 'title', 'table_name': 'posts'},
            {'field_name': 'user_id', 'table_name': 'posts'}
        ]

        self.assertEqual(len(self.list_fields.fields), len(expected_fields))

    def test_multiple_statements(self):
        sql_content = """
        SELECT id, name FROM users;
        SELECT title, content FROM posts;
        """
        self.list_fields.extract_fields(sql_content)
        expected_fields = [
            {'field_name': 'id', 'table_name': 'users'},
            {'field_name': 'name', 'table_name': 'users'},
            {'field_name': 'title', 'table_name': 'posts'},
            {'field_name': 'content', 'table_name': 'posts'}
        ]
        self.assertEqual(self.list_fields.fields, expected_fields)

if __name__ == '__main__':
    unittest.main()
