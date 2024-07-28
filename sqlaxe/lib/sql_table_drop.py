import argparse
import sqlglot
from sqlglot import Dialect
from .sql_formatter import SQLFormatter
from .sql_parser    import SQLParser


class SQLTableDrop:
    def __init__(self, dialect='', output_dialect='', **kwargs):

        self.dialect = dialect
        self.output_dialect = output_dialect or self.dialect

        self.sql_parser    = SQLParser(**kwargs)
        self.sql_formatter = SQLFormatter(pretty_print=True, **kwargs)

    def drop_table(self, sql_content):

        write = Dialect.get_or_raise(self.output_dialect)

        drop_table_tables_statements = []

        expressions = self.sql_parser.parse(sql_content)
        for sql_statement in expressions:
            if sql_statement is None:
                continue
            if sql_statement == "":
                continue

            if (
                isinstance(sql_statement, sqlglot.expressions.Create)
                and sql_statement.kind == "TABLE"
            ):
                table_name = sql_statement.this.this
                drop_table_statement = f"DROP TABLE IF EXISTS {table_name} CASCADE"
                drop_table_tables_statements.append(drop_table_statement)

            if self.output_dialect != self.dialect:
                sql_statement = write.generate(
                    sql_statement, copy=False, pretty=False, identify=False
                )
            else:
                sql_statement = sql_statement.sql(pretty=False, identify=False)

            drop_table_tables_statements.append(sql_statement)

        return drop_table_tables_statements

    def format(self, sql_content):
        statements = self.drop_table(sql_content)

        if len(statements) == 0:
            return ""
        else:
            return ";\n".join(statements) + ";"
