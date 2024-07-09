README.md

# SQLAxe

SQLAxe is a tool for manipulating SQL files. The primary 

Specifically, SQLAxe is a syntax-aware command-line tool implementing the following commands:

1. `split`, for splitting large SQL files into smaller, more manageable files based on the SQL statements they contain. It supports various SQL dialects and provides options for pretty printing and specifying the output directory.

2. `pp`, which re-formats SQL files. It can also transpile from one format to another if you specify different `--dialect` and `--output-dialect` formats.

3. `grep`, which filters SQL files similar to unix `grep`. However, instead of being line-oriented, it parses the SQL file using sqlglot and searches entire statements. If text anywhere in a statement matches, the entire statement is printed out - instead of just the matching line. 

4. `table-name-replace`, which replaces text in table names. It accepts a regular expression for the search text, so you can do something like `sqlaxe table-name-replace ^tbl_ ''`. 

4. `table-truncate`, which prepends a TRUNCATE TABLE command before INSERT INTO statements. This allows you to turn database dumps of INSERT INTO... statements into reusable seed files for development which will clear the table on each load, then insert the data. It will only append TRUNCATE TABLE on the first instance of a table being referenced.

4. `table-drop`, which prepends a DROP TABLE IF EXISTS command before CREATE TABLE statements. This is similar to the `--add-drop-table` option from mysqldump, and can be used to add such statements after the run has completed.

SQLAxe uses sqlglot to parse and output SQL, so it supports a wide variety of dialects of SQL.

![SQLAxe Demo](demo.gif)

```
                                        db                         
                                       d88b                        
    ad88888ba    ,ad8888ba,   88      d8'`8b                       
   d8"     "8b  d8"'    `"8b  88     d8'  `8b                      
   Y8,         d8'        `8b 88    d8YaaaaY8b                     
   `Y8aaaaa,   88          88 88   d8''''''''8b                    
     `"""""8b, 88          88 88  d8'     8b,`bb  ,d8 ,adPPYba,    
           `8b Y8,    "88,,8P 88 d8'       `Y8, ,8P' a8P_____88    
   Y8a     a8P  Y8a.    Y88P  88d8           )888(   8PP""""""'    
    "Y88888P"    `"Y8888Y"Y8a 888888888     d8" "8b, "8b,     ,     
                                          8P'     `Y8 `"Ybbd8"'    
```
                                                                               

## Features

- Split large SQL files into smaller files based on target table.
- Support for multiple SQL dialects (e.g., MySQL, PostgreSQL)
- Option to specify the output SQL dialect
- Customizable output directory
- Pretty printing of SQL statements


## Installation

pip install from pypi (recommended):

`
pip install sqlaxe
`

pip installation from github (edge):

`
pip install git+https://github.com/djberube/sqlaxe
`

Manual installation:

1. Clone the repository:
   ```
   git clone https://github.com/djberube/sqlaxe.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt


## Usage : Split

To split an SQL file using SQLAxe, run the following command:

```
sqlaxe split sql_file.sql
```

Arguments:
- `sql_file`: Path to the SQL file to be split.
- `--dialect DIALECT`: Input SQL dialect (default: mysql).
- `--output-dialect OUTPUT_DIALECT`: Output SQL dialect (defaults to the input dialect).
- `--output-directory OUTPUT_DIRECTORY`: Output directory (defaults to sqlaxe_INPUT_FILENAME, without the extension).
- `--pretty`: Enable pretty printing of SQL statements (default: off).

Example:
```
python sqlaxe.py path/to/your/file.sql --dialect mysql --output-dialect postgresql --output-directory output_files --pretty
```

### Output

SQLAxe will create an output directory (if not specified, it will default to `sqlaxe_INPUT_FILENAME`) and generate separate SQL files for each SQL statement found in the input file. The output files will be named in the format `NNNN_kind.sql`, where `NNNN` is a four-digit section counter and `kind` is the table name or "general" if no table is found.

## Usage: Pretty Print

To pretty print a SQL file, run a command like this:

```
sqlaxe pp sql_file.sql 
```

Arguments:
- `sql_file`: Path to the SQL file to be split.
- `--dialect DIALECT`: Input SQL dialect (default: mysql).
- `--output-dialect OUTPUT_DIALECT`: Output SQL dialect (defaults to the input dialect).


## Usage: grep

To grep a SQL file, run a command like this:

```
sqlaxe grep sql_file.sql PATTERN
```

SQLAxe's grep command is statement oriented, so an entire statement will be printed if it contains PATTERN anywhere within it. This is contrast to the unix grep command, which is line-oriented by default. (Unix grep can be configured with switches to treat, say, NULL as a line terminator - but because SQLAxe parses SQL using sqlglot, it won't be fooled by line terminators or even semicolons inside strings.)

## Usage: table-name-replace

To grep a SQL file, run a command like this:
## Dependencies

- Python 3.x
- sqlglot
- tqdm

## Database Support

- Tested with MySQL and PostgreSQL
- Supports all the dialects from sqlglot; as of this writing, this includes:

    - athena
    - bigquery
    - clickhouse
    - databricks
    - doris
    - drill
    - duckdb
    - hive
    - materialize
    - mysql
    - oracle
    - postgres
    - presto
    - prql
    - redshift
    - risingwave
    - snowflake
    - spark
    - spark2
    - sqlite
    - starrocks
    - tableau
    - teradata
    - trino
    - tsql

## License

This project is licensed under the [MIT License](LICENSE).

## Commercial Support

Commercial support for sqlaxe and related tools is available from Durable Programming, LLC. You can contact us at [durableprogramming.com](https://www.durableprogramming.com).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

