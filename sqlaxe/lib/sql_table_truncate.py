import argparse
import sqlglot
from sqlglot import Dialect


class SQLTableTruncate:
    def __init__(self, **kwargs):
        self.dialect = kwargs["dialect"]
        self.output_dialect = kwargs["output_dialect"] or self.dialect

    def truncate(self, sql_content):
        input_dialect_obj = Dialect.get_or_raise(self.dialect)
        tokens = input_dialect_obj.tokenize(sql_content)
        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)
        sql_statements = parser.parse(raw_tokens=tokens)
        write = Dialect.get_or_raise(self.output_dialect)

        truncate_tables_statements = []
        for sql_statement in sql_statements:
            if sql_statement is None:
                continue
            if sql_statement == "":
                continue

            if isinstance(sql_statement, sqlglot.expressions.Create) and sql_statement.kind == 'TABLE':

                table_name = sql_statement.this.this
                truncate_statement = f"TRUNCATE TABLE {table_name}"
                truncate_tables_statements.append(truncate_statement)

            if self.output_dialect != self.dialect:
                sql_statement = write.generate(
                    sql_statement, copy=False, pretty=False, identify=False
                )
            else:
                sql_statement = sql_statement.sql(pretty=False, identify=False)

            truncate_tables_statements.append(sql_statement)

        return truncate_tables_statements

    def format(self, sql_content):

        statements = self.truncate(sql_content)

        if len(statements) == 0:
            return ''
        else:
            return ";\n".join(statements) + ';'

