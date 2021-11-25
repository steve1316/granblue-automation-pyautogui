import multiprocessing
import time

from utils.settings import Settings
from utils import discord_utils
from bot.game import Game


class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.
    """

    def __init__(self):
        super().__init__()
        self._game = None
        self._bot_process = None
        self._discord_process = None
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
        # #### discord ####
        if Settings.enable_discord and Settings.discord_token != "" and Settings.user_id != 0:
            print("\n[DISCORD] Starting Discord process on a new Thread...")
            self._discord_process = multiprocessing.Process(target = discord_utils.start_now, args = (Settings.discord_token, Settings.user_id, Settings.discord_queue))
            self._discord_process.start()
        else:
            print("\n[DISCORD] Unable to start Discord process. Either you opted not to turn it on or your included token and user id inside the config.ini are invalid.")
        # #### end of discord ####

        print("\n[STATUS] Starting bot on a new Thread...")

        # Create a new Process whose target is the MainDriver's run_bot() method.
        self._bot_process = multiprocessing.Process(target = self._run_bot)

        print("[STATUS] Starting now...")

        # Now start the new Process on a new Thread.
        self._bot_process.start()

        return None

    def stop_bot(self):
        """Stops the bot and terminates the Process.

        Returns:
            None
        """
        if self._bot_process is not None:
            print("\n[STATUS] Stopping the bot and terminating its Thread.")
            self._bot_process.terminate()

        if self._discord_process is not None and self._discord_process.is_alive():
            Settings.discord_queue.put(f"```diff\n- Terminated connection to Discord API for Granblue Automation\n```")
            print("\n[DISCORD] Terminated connection to Discord API and terminating its Thread.")
            time.sleep(1.0)
            self._discord_process.terminate()

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

    MessageLog.print_message("[STATUS] Closing Python process...")
