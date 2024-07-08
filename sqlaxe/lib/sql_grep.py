import argparse
import sqlglot
from sqlglot import Dialect
from .sql_pretty_printer import SQLPrettyPrinter


class SQLGrep(SQLPrettyPrinter):
    def __init__(self, pattern, invert, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.invert = invert

    def format(self, sql_content):
        statements = self.pretty_print_statements(sql_content)
        if self.invert:
            filtered_statements = [
                stmt for stmt in statements if not self.pattern in stmt
            ]
        else:
            filtered_statements = [stmt for stmt in statements if self.pattern in stmt]

        if len(filtered_statements) == 0:
            return ""
        else:
            return ";\n".join(filtered_statements) + ";"
