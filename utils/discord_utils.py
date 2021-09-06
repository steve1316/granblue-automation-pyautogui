import multiprocessing

import discord
from discord import LoginFailure
from discord.ext.tasks import loop


class MyClient:
    """
    Prints and sends all messages in its Queue to the user via Discord private DMs.

    Attributes
    ----------
    bot (discord.Client): The Client object for Discord interaction.

    queue (multiprocessing.Queue): The Queue holding messages to be sent to the user over Discord.

    user_id (int): The User ID on Discord that uniquely identifies them.

    """

    def __init__(self, bot: discord.Client, queue: multiprocessing.Queue, user_id: int):
        self.bot = bot
        self.user = None
        self.user_id = user_id
        self.queue = queue
        self.print_status.start()

    @loop(seconds = 1.0)
    async def print_status(self):
        """Grab each message in the Queue and send it as a private DM to the user.

        Returns:
            None
        """
        if self.user is not None and not self.queue.empty():
            message: str = self.queue.get()
            print(f"[DISCORD] Acquired message to send via Discord DM: {message}")
            await self.user.send(content = message)

    @print_status.before_loop
    async def before_print_status(self):
        """Determine when the bot has successfully connected to the Discord API and found the user.

        Returns:
            None
        """
        print("\n[DISCORD] Waiting for connection to Discord API...")
        await self.bot.wait_until_ready()
        print("[DISCORD] Successful connection to Discord API")
        self.queue.put(f"```diff\n+ Successful connection to Discord API for Granblue Automation\n```")

        try:
            self.user = await self.bot.fetch_user(self.user_id)
            print(f"[DISCORD] Found user: {self.user.name}")
        except discord.errors.NotFound:
            print("[DISCORD] Failed to find user.\n")


def start_now(token: str, user_id: int, queue: multiprocessing.Queue):
    """Initialize the Client object and begin the process to connect to the Discord API.

    Returns:
        None
    """
    client = discord.Client()
    MyClient(client, queue, user_id)
    try:
        client.run(token)
    except LoginFailure:
        print("\n[DISCORD] Failed to connect to Discord API. Please double check your token.\n")
