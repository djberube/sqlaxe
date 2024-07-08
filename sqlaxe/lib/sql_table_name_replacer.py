import os
import argparse
import sqlglot
import re

from sqlglot import parse, Dialect
from sqlglot import expressions as exp
from sqlglot.expressions import Table
from sqlglot.optimizer.scope import traverse_scope
from tqdm import tqdm
from .logger import log


class SQLTableNameReplacer:
    def __init__(self, **kwargs):
        self.dialect = kwargs["dialect"]

        self.output_dialect = kwargs["output_dialect"] or self.dialect
        self.pretty = kwargs["pretty"]
        self.table_name_regex = kwargs["table_name_regex"]
        self.table_name_replacement = kwargs["table_name_replacement"]

    def replace(self, sql_content):
        input_dialect_obj = Dialect.get_or_raise(self.dialect)

        log("tokenizing")

        tokens = input_dialect_obj.tokenize(sql_content)

        log("done tokenizing")

        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)

        write = Dialect.get_or_raise(self.output_dialect)

        sql_statements = parser.parse(raw_tokens=tokens)

        for sql_statement in tqdm(sql_statements, leave=False):
            if sql_statement is None:
                continue
            if sql_statement == "":
                continue

            for node in sql_statement.walk():
                if isinstance(node, exp.Table):
                    old_table_name = node.name
                    new_table_name = re.sub(
                        self.table_name_regex,
                        self.table_name_replacement,
                        old_table_name,
                    )

                    if new_table_name != old_table_name:
                        node.replace(exp.to_table(new_table_name))

                if isinstance(node, exp.Column):
                    old_table_name = node.table
                    new_table_name = re.sub(
                        self.table_name_regex,
                        self.table_name_replacement,
                        old_table_name,
                    )
                    if new_table_name != old_table_name:
                        node.set("table", exp.to_identifier(new_table_name))

            if self.output_dialect != self.dialect:
                print(
                    write.generate(sql_statement, copy=False, pretty=self.pretty)
                    + ";\n"
                )
            else:
                print(sql_statement.sql(pretty=self.pretty) + ";\n")
