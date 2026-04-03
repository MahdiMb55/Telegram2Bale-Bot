import requests

async def download_file(bot, file_id, dest_path):
    file = await bot.get_file(file_id)
    file_path = file.file_path

    url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)