import asyncio
from file_handler import process_file

class Dispatcher:
    def __init__(self, config):
        self.config = config
        self.lock = asyncio.Lock()
        self.bot_index = 0

    async def enqueue(self, event, user_id):
        async with self.lock:
            await process_file(
                event,
                user_id,
                self.config,
                self._get_bot_token()
            )

    def _get_bot_token(self):
        bots = self.config["bale_bots"]
        bot = bots[self.bot_index % len(bots)]
        self.bot_index += 1
        return bot["token"]