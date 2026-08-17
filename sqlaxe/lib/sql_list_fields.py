import csv
import io
import json

import sqlglot
from sqlglot import Dialect, exp

from .sql_parser import SQLParser


class SQLListFields:
    def __init__(self, dialect='', output_format='csv', **kwargs):
        self.dialect = dialect
        self.output_format = output_format
        self.sql_parser = SQLParser(dialect=dialect, **kwargs)
        self.fields = []

    def extract_fields(self, sql_content):
        self.fields = []

        expressions = self.sql_parser.parse(sql_content)
        for sql_statement in expressions:
            if sql_statement is None or sql_statement == "":
                continue

            if isinstance(sql_statement, exp.Create) and sql_statement.kind == "TABLE":
                self._extract_create_table_fields(sql_statement)
            elif isinstance(sql_statement, exp.Select):
                self._extract_select_fields(sql_statement)

        return self.fields

    def _extract_create_table_fields(self, sql_statement):
        table_name = sql_statement.this.this.name
        schema = sql_statement.this

        for column_def in schema.expressions:
            if not isinstance(column_def, exp.ColumnDef):
                continue
            self.fields.append({
                'field_name': column_def.this.name,
                'table_name': table_name,
            })

    def _extract_select_fields(self, sql_statement):
        alias_to_table = {}
        default_table = None
        for table in sql_statement.find_all(exp.Table):
            alias_to_table[table.alias_or_name] = table.name
            if default_table is None:
                default_table = table.name

        for projection in sql_statement.selects:
            column = projection
            if isinstance(column, exp.Alias):
                column = column.this

            if not isinstance(column, exp.Column):
                continue

            if column.table:
                table_name = alias_to_table.get(column.table, column.table)
            else:
                table_name = default_table

            self.fields.append({
                'field_name': column.name,
                'table_name': table_name,
            })

    def format(self, sql_content):
        self.extract_fields(sql_content)

        if self.output_format == 'csv':
            return self._format_csv()
        elif self.output_format == 'jsonl':
            return self._format_jsonl()
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

    def _format_csv(self):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['field_name', 'table_name'])
        writer.writeheader()
        writer.writerows(self.fields)
        return output.getvalue()

    def _format_jsonl(self):
        return "\n".join(json.dumps(field) for field in self.fields)
