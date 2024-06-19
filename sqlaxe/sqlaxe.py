import os
import click
from sqlaxe.lib.sql_splitter import SQLSplitter
from sqlaxe.lib.sql_pretty_printer import SQLPrettyPrinter

@click.group()
def main():
    pass

@main.command()
@click.argument("sql_file", type=click.Path(exists=True))
@click.option("--dialect", type=str, default="mysql", help="Input SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")
@click.option("--output-directory", type=str, default=None, help="output directory (defaults to sqlaxe_INPUT_FILENAME, without the extension)")
def split(sql_file, dialect, output_dialect, output_directory):
    if not output_directory:
        output_directory = "sqlaxe_" + os.path.splitext(os.path.basename(sql_file))[0]

    print(">> reading file")
    with open(sql_file, "r") as file:
        sql_content = file.read()

    splitter = SQLSplitter(
        sql_file=sql_file,
        dialect=dialect,
        output_dialect=output_dialect,
        output_directory=output_directory,
        pretty=False
    )

    splitter.split(sql_content)

@main.command()
@click.argument("sql_file", type=click.Path(exists=True))
@click.option("--dialect", type=str, default="mysql", help="SQL dialect (default: mysql)")
@click.option("--output-dialect", type=str, default=None, help="output SQL dialect (defaults to --dialect)")

def pp(sql_file, dialect, output_dialect):
    print(">> reading file")
    with open(sql_file, "r") as file:
        sql_content = file.read()

    pretty_printer = SQLPrettyPrinter(dialect=dialect, output_dialect=output_dialect)
    pretty_sql = pretty_printer.format(sql_content)

    print(pretty_sql)


if __name__ == "__main__":
    main()
