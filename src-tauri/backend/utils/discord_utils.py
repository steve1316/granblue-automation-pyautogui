import asyncio
import multiprocessing
from typing import Any

import discord
from discord import LoginFailure, Intents

from utils.settings import Settings
from utils.message_log import MessageLog


class MyClient(discord.Client):
    """
    Prints and sends all messages in its Queue to the user via Discord private DMs.

    Attributes
    ----------
    user_id (int): The User ID on Discord that uniquely identifies them.

    queue (multiprocessing.Queue): The Queue holding messages to be sent to the user over Discord.

    test_queue (multiprocessing.Queue, optional): A workaround to notifying the tester that an error occurred. Defaults to None.

    """

    def __init__(self, user_id: int, queue: multiprocessing.Queue, test_queue: multiprocessing.Queue = None, *, intents: Intents, **options: Any):
        super().__init__(intents = intents, **options)
        self.user_id = user_id
        self.queue = queue
        self.test_queue = test_queue
        self.current_user = None
        self.bg_task = None

    async def setup_hook(self) -> None:
        # Async setup after this client connects to the API.
        self.bg_task = self.loop.create_task(self.start_task())

    async def start_task(self):
        """After the connection is ready, continue looping and reading in messages from the queue to send to the user.

        Returns:
            None
        """
        MessageLog.print_message("[DISCORD] Waiting for connection to Discord API...")
        await self.wait_until_ready()
        MessageLog.print_message("[DISCORD] Successful connection to Discord API")
        self.queue.put(f"```diff\n+ Successful connection to Discord API for Granblue Automation\n```")
        if self.test_queue:
            self.test_queue.put("[DISCORD] Successful connection to Discord API")
            self.test_queue.put(f"```diff\n+ Successful connection to Discord API for Granblue Automation\n```")

        try:
            self.current_user = await self.fetch_user(self.user_id)
            MessageLog.print_message(f"[DISCORD] Found user: {self.current_user.name}")
            if self.test_queue:
                self.test_queue.put(f"[DISCORD] Found user: {self.current_user.name}")

            while not self.is_closed():
                if self.current_user is not None and not self.queue.empty():
                    message: str = self.queue.get()
                    if Settings.debug_mode:
                        MessageLog.print_message(f"\n[DEBUG] Acquired message to send via Discord DM: {message}")
                    await self.current_user.send(content = message)

        except discord.errors.HTTPException:
            MessageLog.print_message("[DISCORD] Failed to find user using provided user ID.\n")
            if self.test_queue:
                self.test_queue.put("[DISCORD] Failed to find user using provided user ID.")


def start_now(token: str, user_id: int, queue: multiprocessing.Queue, test_queue: multiprocessing.Queue = None):
    """Initialize the Client object and begin the process to connect to the Discord API.

    Args:
        token (str): Discord Token for use with Discord's API.
        user_id (int): The user's Discord user ID.
        queue (multiprocessing.Queue): The Queue holding messages to be sent to the user over Discord.
        test_queue (multiprocessing.Queue, optional): A workaround to notifying the tester that an error occurred. Defaults to None.

    Returns:
        None
    """
    # Intents is new and required with the migration to discord.py v2.0
    intents = discord.Intents.default()
    intents.dm_messages = True
    client = MyClient(user_id, queue, test_queue, intents = intents)

    try:
        # v2.0 also changed how their event loop works so asyncio is required.
        async def main():
            async with client:
                await client.start(token)

        asyncio.run(main())
        if test_queue:
            test_queue.put("[DISCORD] Successful connection.")
    except LoginFailure:
        MessageLog.print_message("\n[DISCORD] Failed to connect to Discord API using provided token.\n")
        if test_queue:
            test_queue.put("[DISCORD] Failed to connect to Discord API using provided token.")
