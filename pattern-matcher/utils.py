import os

async def save_file_async(file, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, os.path.basename(file.filename))
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    return path
