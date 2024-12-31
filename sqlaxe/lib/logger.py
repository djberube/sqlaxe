# Standard library imports
import inspect
import sys
import time
from datetime import datetime

# Constants for formatting date/time strings and log messages
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MESSAGE_FORMAT = '{timestamp} - {function_name} - {message}'

def log(message: str, log_file: str = 'sqlaxe_events.log', silent: bool = False,
        retries: int = 3, delay: float = 0.1) -> None:
    """
    Log the message with a timestamp to a log file, optionally suppressing terminal output.

    :param message: str - The message to record in log.
    :param log_file: str, optional - Path to the log file. Defaults to 'sqlaxe_events.log'.
    :param silent: bool, optional - If True, suppresses terminal output. Defaults to False.
    :param retries: int, optional - Number of retries if the file is locked. Defaults to 3.
    :param delay: float, optional - Delay in seconds between retries. Defaults to 0.1.

    The function writes the message along with a timestamp to the specified log file.
    If 'silent' is set to False, it will also print the message to the terminal for
    real-time monitoring and debugging.
    """

    # Format the current date and time
    timestamp = datetime.now().strftime(DATE_FORMAT)

    # Get the name of the calling function
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name if frame else "unknown"

    # Format the message with the timestamp and function name
    log_message = LOG_MESSAGE_FORMAT.format(timestamp=timestamp,
                                            function_name=function_name,
                                            message=message)

    # Print the message to the terminal this command will return false when run in an IDE terminal
    if not silent and sys.stdout.isatty():
        print(f'\033[94m>> {message}\033[0m', file=sys.stderr)

    attempt = 0
    while attempt < retries:
        try:
            # Append the message to the log file
            with open(log_file, 'a') as file:
                file.write(log_message + '\n')
            break
        except (OSError, IOError):
            attempt += 1
            time.sleep(delay)