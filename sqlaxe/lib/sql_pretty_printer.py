import argparse
import sqlglot
from sqlglot import Dialect


class SQLPrettyPrinter:
    def __init__(self, **kwargs):
        self.dialect = kwargs["dialect"]
        self.output_dialect = kwargs["output_dialect"] or self.dialect

    def pretty_print_statements(self, sql_content):
        input_dialect_obj = Dialect.get_or_raise(self.dialect)
        tokens = input_dialect_obj.tokenize(sql_content)
        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)
        sql_statements = parser.parse(raw_tokens=tokens)
        write = Dialect.get_or_raise(self.output_dialect)

        pretty_printed_statements = []
        for sql_statement in sql_statements:
            if sql_statement is None:
                continue
            if sql_statement == "":
                continue

            if self.output_dialect != self.dialect:
                pretty_printed_statement = write.generate(
                    sql_statement, copy=False, pretty=True, identify=True
                )
            else:
                pretty_printed_statement = sql_statement.sql(pretty=True, identify=True)

            pretty_printed_statements.append(pretty_printed_statement)

        return pretty_printed_statements

    def format(self, sql_content):
        return ";\n\n".join(self.pretty_print_statements(sql_content)) + ";"
