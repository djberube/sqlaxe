import argparse
import sqlglot
from sqlglot import Dialect, Expression, exp
from .sql_formatter import SQLFormatter
from .sql_parser    import SQLParser


class SQLPrettyPrinter:
    def __init__(self, **kwargs):
        self.sql_parser    = SQLParser(**kwargs)
        self.sql_formatter = SQLFormatter(pretty_print=True, **kwargs)

    def pretty_print_statements(self, sql_content):

        expressions = self.sql_parser.parse(sql_content)
        pretty_print_statements = self.sql_formatter.get_statements(expressions)

        return pretty_print_statements

    def format(self, sql_content):
        return "\n\n".join(self.pretty_print_statements(sql_content))
