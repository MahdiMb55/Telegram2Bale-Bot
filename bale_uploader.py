import aiohttp

BALE_API = "https://tapi.bale.ai/bot{token}/sendDocument"

async def upload_chunks(chunks, chat_id, bot_token):
    async with aiohttp.ClientSession() as session:
        for chunk in chunks:
            with open(chunk, "rb") as f:
                data = aiohttp.FormData()
                data.add_field("chat_id", chat_id)
                data.add_field("document", f)

                url = BALE_API.format(token=bot_token)

                async with session.post(url, data=data) as resp:
                    await resp.text()