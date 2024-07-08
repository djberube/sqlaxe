import os
import argparse
import sqlglot

from sqlglot import parse, Dialect
from sqlglot.expressions import Table
from tqdm import tqdm


class SQLSplitter:
    def __init__(self, **kwargs):
        self.dialect = kwargs["dialect"]

        self.output_dialect = kwargs["output_dialect"] or self.dialect
        self.output_directory = kwargs["output_directory"]
        self.pretty = kwargs["pretty"]

        self.section_counter = 0

    def split(self, sql_content):
        # Get the input dialect object from sqlglot
        input_dialect_obj = Dialect.get_or_raise(self.dialect)

        # Tokenize the SQL content using the input dialect
        print(">> tokenizing")
        tokens = input_dialect_obj.tokenize(sql_content)

        print(">> done tokenizing")

        last_kind = None
        last_output_file = None
        self.section_counter += 1

        # Split the tokens into chunks based on semicolons
        total = len(tokens)
        chunks: t.List[t.List[Token]] = [[]]

        for i, token in enumerate(tqdm(tokens)):
            chunks[-1].append(token)

            if token.token_type == sqlglot.TokenType.SEMICOLON:
                if i < total - 1:
                    chunks.append([])

        statement_counter = 0

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)

        # Create a parser object for the input dialect
        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)

        remainder = iter(tokens)
        row = []
        write = Dialect.get_or_raise(self.output_dialect)

        # Iterate over each chunk of tokens
        for row in tqdm(chunks):
            # Parse the chunk into SQL statements
            sql_statements = parser.parse(raw_tokens=row)

            # Process each SQL statement
            for sql_statement in sql_statements:
                if sql_statement == None:
                    continue

                # Determine the table name or use 'general' if no table is found
                table_name = sql_statement.find(Table)
                kind = table_name.name if table_name else "general"

                # Update section counter and reset statement counter when the kind changes
                if last_kind and last_kind != kind:
                    if statement_counter > 0:
                        print(f"{statement_counter} statements")
                    self.section_counter += 1
                    statement_counter = 0

                # Generate the output file path based on the section counter and kind
                output_file = os.path.join(
                    self.output_directory, f"{self.section_counter:04}_{kind}.sql"
                )
                output_file_has_changed = last_output_file != output_file

                # Write the SQL statement to the output file
                with open(output_file, "a") as file:
                    if output_file_has_changed:
                        print(f">> writing to {output_file}")
                        file.truncate(0)

                    if self.output_dialect != self.dialect:
                        file.write(
                            write.generate(
                                sql_statement, copy=False, pretty=self.pretty
                            )
                            + ";\n"
                        )
                    else:
                        file.write(sql_statement.sql(pretty=self.pretty) + ";\n")

                last_output_file = output_file
                last_kind = kind
                statement_counter += 1
