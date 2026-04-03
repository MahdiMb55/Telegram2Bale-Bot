import requests
import json

with open("config.json") as f:
    config = json.load(f)

async def download_file(bot, file_id, dest_path):

    tg_file = await bot.get_file(file_id)
    print("FILE ID:", file_id)
    print("FILE PATH:", tg_file.file_path)

    if not tg_file.file_path:
        raise Exception("file_path is empty (Telegram returned invalid file)")

    token = config["telegram_bot_token"]

    url = f"https://api.telegram.org/file/bot{token}/{tg_file.file_path}"

    r = requests.get(url, stream=True)

    if r.status_code != 200:
        raise Exception(f"Download failed: {r.text}")

    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)