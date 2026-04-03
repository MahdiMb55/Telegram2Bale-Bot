from telethon import TelegramClient, events
import os


class TelegramListener:
    def __init__(self, config, dispatcher):
        self.config = config
        self.dispatcher = dispatcher

        self.client = TelegramClient(
            config["telegram"]["session"],
            config["telegram"]["api_id"],
            config["telegram"]["api_hash"],
        )

    async def start(self):
        @self.client.on(events.NewMessage)
        async def handler(event):
            user_id = str(event.sender_id)

            if user_id not in self.config["user_map"]:
                return

            if event.message.media:
                await self.dispatcher.enqueue(event, user_id)

        await self.client.start()
        await self.client.run_until_disconnected()