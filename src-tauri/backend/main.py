import multiprocessing
import time

from utils.message_log import MessageLog
from bot.game import Game


class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.
    """

    def __init__(self):
        super().__init__()
        self._game = None
        self._bot_process = None

    def is_running(self) -> bool:
        """Check the status of the bot process.

        Returns:
            (bool): Flag that indicates whether the bot process is still running or not.
        """
        return self._bot_process.is_alive()

    def _run_bot(self):
        """Starts the main bot process on this Thread.

        Returns:
            None
        """
        # Initialize the Game class and start Farming Mode.
        self._game = Game()
        self._game.start_farming_mode()
        return None

    def start_bot(self):
        """Starts the bot's Game class on a new Thread.

        Returns:
            None
        """
        # Create a new Process whose target is the MainDriver's run_bot() method.
        self._bot_process = multiprocessing.Process(target = self._run_bot)

        MessageLog.print_message("[STATUS] Starting bot process on a new thread now...")

        # Now start the new Process on a new Thread.
        self._bot_process.start()
        self._bot_process.is_alive()

        return None

    def stop_bot(self):
        """Stops the bot and terminates the Process.

        Returns:
            None
        """
        if self._bot_process is not None:
            MessageLog.print_message("\n[STATUS] Stopping the bot and terminating its Thread.")
            self._bot_process.terminate()

        return None


if __name__ == "__main__":
    # Start the bot.
    bot_object = MainDriver()
    bot_object.start_bot()

    while True:
        if bot_object.is_running() is False:
            break
        else:
            time.sleep(1.0)

    bot_object.stop_bot()

    time.sleep(1.0)
    MessageLog.print_message("[STATUS] Closing Python process...")
