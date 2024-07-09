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

        truncated_tables = []
        truncate_tables_statements = []

        for sql_statement in sql_statements:
            if sql_statement is None:
                continue
            if sql_statement == "":
                continue


            if isinstance(sql_statement, sqlglot.expressions.Insert):
                table_name = sql_statement.this.this
                if table_name not in truncated_tables:
                    truncate_statement = f"TRUNCATE TABLE {table_name}"
                    parsed = input_dialect_obj.parse(truncate_statement)
                    truncate_tables_statements.append(parsed[0])
                    truncated_tables.append(table_name)

            truncate_tables_statements.append(sql_statement)

        return truncate_tables_statements

    def format(self, sql_content):


        write = Dialect.get_or_raise(self.output_dialect)
        statements = self.truncate(sql_content)

        out = []
        for sql_statement in statements:
            if self.output_dialect != self.dialect:
                out.append(write.generate(
                    sql_statement, copy=False, pretty=True, identify=True
                ))
            else:
                out.append( sql_statement.sql(pretty=True, identify=True) )

        if len(out) == 0:
            return ''
        else:
            return ";\n".join(out) + ';'
