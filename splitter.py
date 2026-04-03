import os

def split_file(file_path, output_dir, chunk_size_mb):
    chunk_size = chunk_size_mb * 1024 * 1024
    parts = []

    with open(file_path, "rb") as f:
        index = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            part_name = os.path.join(output_dir, f"part_{index:03d}")
            with open(part_name, "wb") as pf:
                pf.write(chunk)

            parts.append(part_name)
            index += 1

    return parts