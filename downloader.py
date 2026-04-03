import requests
import json

with open("config.json") as f:
    config = json.load(f)

async def download_file(bot, file_id, dest_path):
    file = await bot.get_file(file_id)
    print(file.file_path)

    token = config["telegram_bot_token"]
    url = f"https://api.telegram.org/file/bot{token}/{file.file_path}"

    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            raise Exception(f"Download failed: {r.text}")

        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)