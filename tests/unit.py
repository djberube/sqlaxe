import unittest
import os
import shutil

from sqlaxe.lib.sql_splitter import SQLSplitter


class TestSQLSplitter(unittest.TestCase):
    def setUp(self):
        self.sql_file = "test.sql"
        self.dialect = "mysql"
        self.output_dialect = "mysql"
        self.output_directory = "test_output"
        self.pretty = True
        self.splitter = SQLSplitter(
            dialect=self.dialect,
            output_dialect=self.output_dialect,
            output_directory=self.output_directory,
            pretty=self.pretty,
        )

    def tearDown(self):
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

    def test_init(self):
        self.assertEqual(self.splitter.dialect, self.dialect)
        self.assertEqual(self.splitter.output_dialect, self.output_dialect)
        self.assertEqual(self.splitter.output_directory, self.output_directory)
        self.assertEqual(self.splitter.pretty, self.pretty)

    def test_split(self):
        test_sql = "SELECT * from table1; SELECT * FROM table2;"

        self.splitter.split(test_sql)

        print(os.path.realpath(self.output_directory))

        self.assertTrue(os.path.exists(self.output_directory))
        self.assertTrue(
            os.path.exists(os.path.join(self.output_directory, "0001_table1.sql"))
        )

        with open(os.path.join(self.output_directory, "0001_table1.sql"), "r") as file:
            content = file.read()
            self.assertIn("SELECT\n  *\nFROM table1;\n", content)

        self.assertTrue(
            os.path.exists(os.path.join(self.output_directory, "0002_table2.sql"))
        )

        with open(os.path.join(self.output_directory, "0002_table2.sql"), "r") as file:
            content = file.read()
            self.assertIn("SELECT\n  *\nFROM table2;\n", content)


if __name__ == "__main__":
    unittest.main()
