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
#  Python script for a command-line tool called sqlaxe. The tool processes SQL files, and can perform tasks such as splitting SQL statements, pretty printing SQL code, searching for specific patterns, replacing table names, truncating tables, and dropping tables.
#

import os
import click

from .lib.sql_splitter import SQLSplitter
from .lib.sql_pretty_printer import SQLPrettyPrinter
from .lib.sql_table_name_replacer import SQLTableNameReplacer
from .lib.sql_table_truncate import SQLTableTruncate
from .lib.sql_table_drop import SQLTableDrop
from .lib.sql_grep import SQLGrep
from .lib.logger import log

import sys
import logging

# Set logging level for sqlglot to ERROR
logging.getLogger("sqlglot").setLevel(logging.ERROR)

# Main click group
@click.group()
def main():
    pass

# Command: split
@main.command()
@click.argument("sql_file", type=click.File())
@click.option("--dialect", type=str, default="mysql", help="Input SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
@click.option("--output-directory", type=str, default=None, help="output directory (defaults to sqlaxe_INPUT_FILENAME, without the extension)")
def split(sql_file, dialect, output_dialect, output_directory):
    # Set default output directory if not provided
    if not output_directory:
        output_directory = "sqlaxe_" + os.path.splitext(os.path.basename(sql_file))[0]

    log("reading file")
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
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
def pp(sql_file, dialect, output_dialect):
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
def grep(sql_file, pattern, dialect, output_dialect, invert):
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
def table_name_replace(sql_file, table_name_regex, table_name_replacement, dialect, output_dialect):
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
def table_truncate(sql_file, dialect, output_dialect):
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
def table_drop(sql_file, dialect, output_dialect):
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
