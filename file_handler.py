import os
import uuid
import shutil
from chunker import zip_and_split
from bale_uploader import upload_chunks

async def process_file(event, user_id, config, bot_token):
    temp_dir = config["temp_dir"]
    os.makedirs(temp_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    input_path = await event.message.download_media(file=temp_dir)
    
    await event.message.download_media(file=input_path)
    print("downloaded !")
    chunks = zip_and_split(
        input_path,
        temp_dir,
        config["chunk_size_mb"]
    )
    print("chuncked !")

    await upload_chunks(
        chunks,
        config["user_map"][user_id],
        bot_token
    )

    shutil.rmtree(input_path, ignore_errors=True)

    for c in chunks:
        try:
            os.remove(c)
        except:
            pass