import requests
import os

def download_file(bot, file_id, dest_path):
    file = bot.get_file(file_id)
    url = file.file_path

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)