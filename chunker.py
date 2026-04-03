import os
import zipfile
import math

def zip_and_split(file_path, out_dir, chunk_size_mb):
    zip_path = file_path + ".zip"

    # ZIP file
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(file_path, arcname=os.path.basename(file_path))

    chunk_size = chunk_size_mb * 1024 * 1024

    chunks = []
    part_num = 0

    with open(zip_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break

            part_path = f"{zip_path}.part{part_num}"
            with open(part_path, "wb") as pf:
                pf.write(data)

            chunks.append(part_path)
            part_num += 1

    os.remove(zip_path)
    return chunks