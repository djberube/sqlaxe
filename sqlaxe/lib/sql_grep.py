import argparse
import sqlglot
from sqlglot import Dialect
from lib.sql_pretty_printer import SQLPrettyPrinter

class SQLGrep(SQLPrettyPrinter):

    def __init__(self, pattern, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

    def format(self, sql_content):

        statements = self.pretty_print_statements(sql_content)
        filtered_statements = [stmt for stmt in statements if self.pattern in stmt]

        return ';\n'.join(filtered_statements) + ';'

