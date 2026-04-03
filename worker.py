import os
import json
import shutil
from downloader import download_file
from splitter import split_file
from uploader import upload_to_bale

with open("config.json") as f:
    config = json.load(f)

def process_file(bot, file_id, file_name, telegram_user_id):
    temp_dir = config["temp_dir"]
    os.makedirs(temp_dir, exist_ok=True)

    user_dir = os.path.join(temp_dir, file_id)
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, file_name)

    # دانلود
    await download_file(bot, file_id, file_path)

    # split
    parts = split_file(file_path, user_dir, config["chunk_size_mb"])

    # upload (round robin)
    bale_chat_id = config["user_map"][telegram_user_id]
    bots = config["bale_bots"]

    for i, part in enumerate(parts):
        bot_token = bots[i % len(bots)]["token"]

        retry = 3
        while retry > 0:
            try:
                upload_to_bale(part, bot_token, bale_chat_id)
                break
            except Exception:
                retry -= 1
                if retry == 0:
                    raise

    # cleanup
    shutil.rmtree(user_dir)