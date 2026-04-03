import aiohttp
import asyncio

BALE_API = "https://tapi.bale.ai/bot{token}/sendDocument"

async def upload_chunks(chunks, chat_id, bot_token):
    timeout = aiohttp.ClientTimeout(total=120)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for chunk in chunks:

            for attempt in range(3):
                try:
                    with open(chunk, "rb") as f:
                        data = aiohttp.FormData()
                        data.add_field("chat_id", chat_id)
                        data.add_field("document", f)

                        url = BALE_API.format(token=bot_token)

                        async with session.post(url, data=data) as resp:
                            text = await resp.text()

                            if resp.status == 200:
                                break
                            else:
                                raise Exception(text)

                except Exception as e:
                    if attempt == 2:
                        raise e

                    await asyncio.sleep(2 * (attempt + 1))