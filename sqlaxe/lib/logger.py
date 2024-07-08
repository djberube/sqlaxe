import sys


def log(message):
    print(f"\033[94m>> {message}\033[0m", file=sys.stderr)
