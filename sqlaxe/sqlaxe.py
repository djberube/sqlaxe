#             _                
#   ___  __ _| | __ ___  _____ 
#  / __|/ _` | |/ _` \ \/ / _ \
#  \__ \ (_| | | (_| |>  <  __/
#  |___/\__, |_|\__,_/_/\_\___|
#          |_|                 
#  ----------------------------
#  file: sqlaxe.py
#  ----------------------------
#
# Python script for a command-line tool called sqlaxe. The tool processes SQL files, and can perform tasks such as
# splitting SQL statements, pretty printing SQL code, searching for specific patterns, replacing table names,
# truncating tables, and dropping tables.
#

import logging
import os
from typing import Optional, TextIO

import click

from sqlaxe.lib.logger import log
from sqlaxe.lib.sql_grep import SQLGrep
from sqlaxe.lib.sql_pretty_printer import SQLPrettyPrinter
from sqlaxe.lib.sql_splitter import SQLSplitter
from sqlaxe.lib.sql_table_drop import SQLTableDrop
from sqlaxe.lib.sql_table_name_replacer import SQLTableNameReplacer
from sqlaxe.lib.sql_table_truncate import SQLTableTruncate

# Set logging level for sqlglot to ERROR
logging.getLogger("sqlglot").setLevel(logging.ERROR)

# Main click group
@click.group()
def main() -> None:
    """Entry point for the SQLAxe command-line tool."""
    pass

# Command: split
@main.command()
@click.argument("sql_file", type=click.File())
@click.option("--dialect", type=str, default="mysql", help="Input SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None,
              help="output SQL dialect (defaults to --dialect)")
@click.option("--output-directory", type=str, default=None,
              help="output directory (defaults to sqlaxe_INPUT_FILENAME, without the extension)")
def split(sql_file: TextIO, dialect: str, output_dialect: str, output_directory: Optional[str]) -> None:
    """
    Split SQL file into individual statements.

    :param sql_file: SQL file to be processed.
    :param dialect: Input SQL dialect.
    :param output_dialect: Output SQL dialect.
    :param output_directory: Directory for output files.
    """

    # Set default output directory if not provided
    if not output_directory:
        output_directory = "sqlaxe_" + os.path.splitext(os.path.basename(sql_file.name))[0]

    log("Reading the contents of file to memory")

    sql_content = sql_file.read()

    # Create SQLSplitter instance and split the SQL content
    splitter = SQLSplitter(
        sql_file=sql_file,
        dialect=dialect,
        output_dialect=output_dialect,
        output_directory=output_directory,
        pretty=False,
    )
    splitter.split(sql_content)

# Command: pp (Pretty Print)
@main.command()
@click.argument("sql_file", type=click.File())
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None,
              help="output SQL dialect (defaults to --dialect)")
def pp(sql_file: TextIO, dialect: str, output_dialect: Optional[str]) -> None:
    log("reading file")
    sql_content = sql_file.read()

    # Create SQLPrettyPrinter instance and format the SQL content
    pretty_printer = SQLPrettyPrinter(dialect=dialect, output_dialect=output_dialect)
    pretty_sql = pretty_printer.format(sql_content)

    print(pretty_sql)

# Command: grep
@main.command()
@click.argument("sql_file", type=click.File("r"))
@click.argument("pattern", type=str)
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
@click.option("--invert/--no-invert", default=False, help="inverts match, so that only non-matching lines appear")
def grep(sql_file: TextIO, pattern: str, dialect: str, output_dialect: Optional[str], invert: bool) -> None:
    """
    Search for a pattern in SQL file.

    :param sql_file: SQL file to search.
    :param pattern: Pattern to search for.
    :param dialect: SQL dialect.
    :param output_dialect: Output SQL dialect.
    :param invert: Invert match to show only non-matching lines.
    """
    log("reading file")
    sql_content = sql_file.read()

    # Create SQLGrep instance and format the SQL content
    pretty_printer = SQLGrep(
        pattern=pattern, dialect=dialect, output_dialect=output_dialect, invert=invert
    )
    pretty_sql = pretty_printer.format(sql_content)

    print(pretty_sql)

# Command: table_name_replace
@main.command()
@click.argument("sql_file", type=click.File("r"))
@click.argument("table_name_regex", type=str)
@click.argument("table_name_replacement", type=str)
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
def table_name_replace(sql_file: TextIO, table_name_regex: str, table_name_replacement: str, dialect: str,
                       output_dialect: Optional[str]) -> None:
    """
    Replace table names in SQL file based on a regex pattern.

    :param sql_file: SQL file to process.
    :param table_name_regex: Regex pattern to match table names.
    :param table_name_replacement: Replacement string for matched table names.
    :param dialect: SQL dialect.
    :param output_dialect: Output SQL dialect.
    """
    log("reading file")
    sql_content = sql_file.read()

    # Create SQLTableNameReplacer instance and replace table names
    replacer = SQLTableNameReplacer(
        table_name_regex=table_name_regex,
        table_name_replacement=table_name_replacement,
        dialect=dialect,
        output_dialect=output_dialect,
        pretty=False,
    )
    replacer.replace(sql_content)

# Command: table_truncate
@main.command()
@click.argument("sql_file", type=click.File("r"))
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
def table_truncate(sql_file: TextIO, dialect: str, output_dialect: Optional[str]) -> None:
    """
    Generate SQL to truncate tables.

    :param sql_file: SQL file to process.
    :param dialect: SQL dialect.
    :param output_dialect: Output SQL dialect.
    """
    log("reading file")
    sql_content = sql_file.read()

    # Create SQLTableTruncate instance and format the SQL content
    truncator = SQLTableTruncate(
        dialect=dialect,
        output_dialect=output_dialect,
        pretty=False,
    )
    print(truncator.format(sql_content))

# Command: table_drop
@main.command()
@click.argument("sql_file", type=click.File("r"))
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
def table_drop(sql_file: TextIO, dialect: str, output_dialect: Optional[str]) -> None:
    """
    Generate SQL to drop tables.

    :param sql_file: SQL file to process.
    :param dialect: SQL dialect.
    :param output_dialect: Output SQL dialect.
    """
    log("reading file")
    sql_content = sql_file.read()

    # Create SQLTableDrop instance and format the SQL content
    truncator = SQLTableDrop(
        dialect=dialect,
        output_dialect=output_dialect,
        pretty=False,
    )
    print(truncator.format(sql_content))

if __name__ == "__main__":
    main()