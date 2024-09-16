import sys


def log(message):
    if sys.stdout.isatty():
        print(f"\033[94m>> {message}\033[0m", file=sys.stderr)
