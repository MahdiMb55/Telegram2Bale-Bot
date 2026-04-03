import asyncio
from telegram_client import TelegramListener
from dispatcher import Dispatcher
from config import load_config

async def main():
    config = load_config()

    dispatcher = Dispatcher(config)
    tg = TelegramListener(config, dispatcher)

    await tg.start()

if __name__ == "__main__":
    asyncio.run(main())