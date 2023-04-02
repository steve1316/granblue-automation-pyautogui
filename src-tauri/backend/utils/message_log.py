import datetime
from timeit import default_timer as timer
import inspect
import logging
import sys


class MessageLog:
    """
    Provides utility functions to print for the message log.
    """

    _starting_time = timer()

    enable_inspect_caller = False

    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    @staticmethod
    def _print_time():
        """Formats the time since the bot started into a readable, printable HH:MM:SS format using timedelta.

        Returns:
            str: A formatted string that displays the elapsed time since the bot started.
        """
        return str(datetime.timedelta(seconds = (timer() - MessageLog._starting_time))).split('.')[0]

    @staticmethod
    def print_message(message: str):
        """Listen for and format messages before printing it to console.

        Returns:
            None
        """
        # Loop until the status flag has been set to 1.
        if message.startswith("\n"):
            if MessageLog.enable_inspect_caller:
                new_message = "\n" + MessageLog._print_time() + " " + f"[{inspect.stack()[1][3]}]" + message[len("\n"):]
            else:
                new_message = "\n" + MessageLog._print_time() + " " + message[len("\n"):]
        else:
            if MessageLog.enable_inspect_caller:
                new_message = MessageLog._print_time() + " " + f"[{inspect.stack()[1][3]}]" + message
            else:
                new_message = MessageLog._print_time() + " " + message

        try:
            logging.info(new_message)
        except UnicodeEncodeError:
            # Clean out any non UTF-8 characters before printing.
            new_message_decoded = new_message.encode("utf-8", "ignore")
            logging.info(new_message_decoded)

        return None
