import datetime
from timeit import default_timer as timer


class MessageLog:
    """
    Provides utility functions to print for the message log.
    """

    _starting_time = timer()

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
            new_message = "\n" + MessageLog._print_time() + " " + message[len("\n"):]
        else:
            new_message = MessageLog._print_time() + " " + message

        print(new_message, flush = True)

        return None
