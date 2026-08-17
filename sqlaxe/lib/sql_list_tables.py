import csv
import io
import json

from sqlglot import exp

from .sql_parser import SQLParser


class SQLListTables:
    def __init__(self, dialect='', output_format='csv', **kwargs):
        self.dialect = dialect
        self.output_format = output_format
        self.sql_parser = SQLParser(dialect=dialect, **kwargs)
        self.tables = []

    def extract_tables(self, sql_content):
        seen = set()
        self.tables = []

        expressions = self.sql_parser.parse(sql_content)
        for sql_statement in expressions:
            if sql_statement is None or sql_statement == "":
                continue

            for table in sql_statement.find_all(exp.Table):
                table_name = table.name
                if not table_name or table_name in seen:
                    continue
                seen.add(table_name)
                self.tables.append(table_name)

        return self.tables

    def format(self, sql_content):
        self.extract_tables(sql_content)

        if self.output_format == 'csv':
            return self._format_csv()
        elif self.output_format == 'jsonl':
            return self._format_jsonl()
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

    def _format_csv(self):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['table_name'])
        writer.writeheader()
        for table_name in self.tables:
            writer.writerow({'table_name': table_name})
        return output.getvalue()

    def _format_jsonl(self):
        return "\n".join(json.dumps({'table_name': table_name}) for table_name in self.tables)
