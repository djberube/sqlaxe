import unittest
from sqlaxe.lib.sql_pretty_printer import SQLPrettyPrinter

class TestSQLPrettyPrinter(unittest.TestCase):
    def setUp(self):
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.pretty_printer = SQLPrettyPrinter(
            dialect=self.dialect,
            output_dialect=self.output_dialect,
        )

    def test_pretty_print_select(self):
        sql_content = "SELECT * FROM table1 WHERE id = 1;"
        expected_output = 'SELECT\n  *\nFROM "table1"\nWHERE\n  "id" = 1;'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_insert(self):
        sql_content = "INSERT INTO table1 (id, name) VALUES (1, 'John');"
        expected_output = 'INSERT INTO "table1" (\n  "id",\n  "name"\n)\nVALUES\n  (1, \'John\');'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_update(self):
        sql_content = "UPDATE table1 SET name = 'Jane' WHERE id = 1;"
        expected_output = 'UPDATE "table1" SET "name" = \'Jane\'\nWHERE\n  "id" = 1;'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_delete(self):
        sql_content = "DELETE FROM table1 WHERE id = 1;"
        expected_output = 'DELETE FROM "table1"\nWHERE\n  "id" = 1;'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_create_table(self):
        sql_content = "CREATE TABLE table1 (id INT PRIMARY KEY, name VARCHAR(50));"
        expected_output = 'CREATE TABLE "table1" (\n  "id" INT PRIMARY KEY,\n  "name" VARCHAR(50)\n);'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_multiple_statements(self):
        sql_content = "SELECT * FROM table1; INSERT INTO table2 VALUES (1, 'Test');"
        expected_output = 'SELECT\n  *\nFROM "table1";\n\nINSERT INTO "table2"\nVALUES\n  (1, \'Test\');'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)

    def test_pretty_print_different_output_dialect(self):
        self.pretty_printer.sql_formatter.output_dialect = "postgres"
        sql_content = "SELECT * FROM table1;"
        expected_output = 'SELECT\n  *\nFROM "table1";'
        result = self.pretty_printer.format(sql_content)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
