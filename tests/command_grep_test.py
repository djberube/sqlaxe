import unittest
import os

from sqlaxe.lib.sql_grep import SQLGrep

class TestSQLGrep(unittest.TestCase):
    def setUp(self):
        self.sql_file = "test.sql"
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.grep = SQLGrep(
            pattern="table1",
            dialect=self.dialect,
            output_dialect=self.output_dialect,
            invert=False,
        )

    def tearDown(self):
        return True

    def test_grep(self):
        test_sql = (
            "SELECT * from table1; SELECT * FROM table2; SELECT \n\t\tid FROM table1;"
        )
        pattern = "SELECT \* FROM table1"

        content = self.grep.format(test_sql)

        self.assertIn('SELECT\n  *\nFROM "table1";\n', content)
        self.assertIn('SELECT\n  "id"\nFROM "table1";', content)
        self.assertNotIn('SELECT\n  *\nFROM "table2";\n', content)

    def test_postgresql_dialect(self):
        self.grep = SQLGrep(
            pattern="table1",
            dialect="postgres",
            output_dialect="postgres",
            invert=False,
        )
        test_sql = "SELECT * FROM table1; CREATE TABLE table2 (id SERIAL PRIMARY KEY);"
        content = self.grep.format(test_sql)
        self.assertIn('SELECT\n  *\nFROM "table1";', content)
        self.assertNotIn('CREATE TABLE "table2"', content)

    def test_oracle_dialect(self):
        self.grep = SQLGrep(
            pattern="table1",
            dialect="oracle",
            output_dialect="oracle",
            invert=False,
        )
        test_sql = "SELECT * FROM table1; CREATE TABLE table2 (id NUMBER PRIMARY KEY);"
        content = self.grep.format(test_sql)
        self.assertIn('SELECT\n  *\nFROM "table1";', content)
        self.assertNotIn('CREATE TABLE "table2"', content)

    def test_create_table(self):
        test_sql = "CREATE TABLE table1 (id INT PRIMARY KEY); CREATE TABLE table2 (id INT PRIMARY KEY);"
        content = self.grep.format(test_sql)
        self.assertEqual('CREATE TABLE "table1" (\n  "id" INT PRIMARY KEY\n);', content)

    def test_insert_statement(self):
        test_sql = "INSERT INTO table1 VALUES (1); INSERT INTO table2 VALUES (2);"
        content = self.grep.format(test_sql)
        self.assertEqual('INSERT INTO "table1"\nVALUES\n  (1);', content)

    def test_drop_table(self):
        test_sql = "DROP TABLE table1; DROP TABLE table2;"
        content = self.grep.format(test_sql)
        self.assertIn('DROP TABLE "table1"', content)
        self.assertNotIn('DROP TABLE "table2"', content)

    def test_alter_table(self):
        test_sql = "ALTER TABLE table1 ADD new_col INT; ALTER TABLE table2 DROP COLUMN old_col;"
        content = self.grep.format(test_sql)
        self.assertIn('ALTER TABLE "table1"', content)
        self.assertNotIn('ALTER TABLE "table2"', content)

    def test_update_statement(self):
        test_sql = "UPDATE table1 SET col = 1; UPDATE table2 SET col = 2;"
        content = self.grep.format(test_sql)
        self.assertIn('UPDATE "table1"', content)
        self.assertNotIn('UPDATE "table2"', content)

    def test_create_table_with_multiple_columns(self):
        test_sql = """
        CREATE TABLE table1 (
            id INT PRIMARY KEY,
            name VARCHAR(50),
            age INT
        );
        CREATE TABLE table2 (
            id INT PRIMARY KEY,
            description TEXT
        );
        """
        content = self.grep.format(test_sql)
        self.assertEqual('CREATE TABLE "table1" (\n  "id" INT PRIMARY KEY,\n  "name" VARCHAR(50),\n  "age" INT\n);', content)
        self.assertNotIn('CREATE TABLE "table2"', content)

    def test_insert_statement_with_column_names(self):
        test_sql = """
        INSERT INTO table1 (id, name, age) VALUES (1, 'John', 30);
        INSERT INTO table2 (id, description) VALUES (1, 'Test description');
        """
        content = self.grep.format(test_sql)
        self.assertEqual('INSERT INTO "table1" (\n  "id",\n  "name",\n  "age"\n)\nVALUES\n  (1, \'John\', 30);', content)
        self.assertNotIn('INSERT INTO "table2"', content)

    def test_drop_table_with_cascade(self):
        test_sql = """
        DROP TABLE table1 CASCADE;
        DROP TABLE table2 CASCADE;
        """
        content = self.grep.format(test_sql)
        self.assertIn('DROP TABLE "table1" CASCADE', content)
        self.assertNotIn('DROP TABLE "table2"', content)


    def test_complex_select_statement(self):
        test_sql = """
        SELECT t1.id, t1.name, t2.description
        FROM table1 t1
        LEFT JOIN table2 t2 ON t1.id = t2.id
        WHERE t1.age > 30
        ORDER BY t1.name;
        """
        content = self.grep.format(test_sql)
        self.assertEqual('SELECT\n  "t1"."id",\n  "t1"."name",\n  "t2"."description"\nFROM "table1" AS "t1"\nLEFT JOIN "table2" AS "t2"\n  ON "t1"."id" = "t2"."id"\nWHERE\n  "t1"."age" > 30\nORDER BY\n  "t1"."name";', content)

if __name__ == "__main__":
    unittest.main()
