import multiprocessing
from datetime import datetime

import discord
from discord.ext.tasks import loop


class MyClient:
    def __init__(self, bot: discord.Client, queue, user_id: int):
        self.bot = bot
        self.user = None
        self.user_id = user_id
        self.queue = queue
        self.print_status.start()

    @loop(seconds = 1.0)
    async def print_status(self):
        if self.user is None:
            self.user = await self.bot.fetch_user(self.user_id)
            print(f"Found user: {self.user.name}")

        if not self.queue.empty():
            message: str = self.queue.get()
            print(f"Acquired message to send via Discord DM: {message}")
            await self.user.send(content = message)

    @print_status.before_loop
    async def before_print_status(self):
        print("Waiting for connection to Discord API...")
        await self.bot.wait_until_ready()
        print("Connection to Discord API successful!")
        now = datetime.now()
        self.queue.put(f"--------------------\n[{now.strftime('%I:%M:%S')}]Connection to Discord API successful!")


def start_now(token: str, user_id: int, queue: multiprocessing.Queue):
    client = discord.Client()
    MyClient(client, queue, user_id)
    client.run(token)
