import argparse
import sqlglot
from tqdm import tqdm
from sqlglot import Dialect, Expression, exp


class SQLParser:
    def __init__(self, **kwargs):
        self.dialect = kwargs["dialect"]

    def parse(self, sql_content):
        input_dialect_obj = Dialect.get_or_raise(self.dialect)
        tokens = input_dialect_obj.tokenize(sql_content)
        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)
        sql_statements = parser.parse(raw_tokens=tokens)

        # Get the input dialect object from sqlglot
        input_dialect_obj = Dialect.get_or_raise(self.dialect)

        # Tokenize the SQL content using the input dialect
        tokens = input_dialect_obj.tokenize(sql_content)


        # Split the tokens into chunks based on semicolons
        total = len(tokens)
        chunks: t.List[t.List[Token]] = [[]]

        for i, token in enumerate(tqdm(tokens)):
            chunks[-1].append(token)

            if token.token_type == sqlglot.TokenType.SEMICOLON:
                if i < total - 1:
                    chunks.append([])

        statement_counter = 0

        # Create a parser object for the input dialect
        parser = input_dialect_obj.parser(error_level=sqlglot.errors.ErrorLevel.IGNORE)

        remainder = iter(tokens)

        output = []
        # Iterate over each chunk of tokens
        for row in tqdm(chunks):
            # Parse the chunk into SQL statements
            sql_statements = parser.parse(raw_tokens=row)

            if sql_statements:

                for statement in sql_statements:
                    output.append(statement)

            else:
                output.append(chunk)



        return output

