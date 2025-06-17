import os
import aiohttp
import zipfile
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# URLs des microservices
ANNOTATOR_URL = os.getenv("ANNOTATOR_URL", "http://localhost:8001")
MATCHING_API_URL = os.getenv("MATCHING_API_URL", "http://localhost:8002")
TRACKING_API_URL = os.getenv("TRACKING_API_URL", "http://localhost:8003")
SCENE_API_URL = os.getenv("SCENE_API_URL", "http://localhost:8004")
FACE_API_URL = os.getenv("FACE_API_URL", "http://localhost:8005")

async def fetch_data_as_zip(session, url, user_id):
    headers = {"user_id": user_id}
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise Exception(f"Erreur lors de l'appel à {url}: {resp.status}")
        return await resp.read()

async def generate_user_export_zip(user_id: str) -> bytes:
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        async with aiohttp.ClientSession() as session:
            # 1. Annotation Service
            try:
                zip_data = await fetch_data_as_zip(session, f"{ANNOTATOR_URL}/export", user_id)
                zipf.writestr("annotation.zip", zip_data)
            except Exception as e:
                print(f"Annotation export failed: {e}")

            # 2. Matching Service
            try:
                zip_data = await fetch_data_as_zip(session, f"{MATCHING_API_URL}/export", user_id)
                zipf.writestr("matching.json", zip_data)
            except Exception as e:
                print(f"Matching export failed: {e}")

            # 3. Tracking Service
            try:
                zip_data = await fetch_data_as_zip(session, f"{TRACKING_API_URL}/export", user_id)
                zipf.writestr("tracking.json", zip_data)
            except Exception as e:
                print(f"Tracking export failed: {e}")

            # 4. Scene Splitter (scenes + frames)
            try:
                zip_data = await fetch_data_as_zip(session, f"{SCENE_API_URL}/export", user_id)
                zipf.writestr("scene_split.json", zip_data)
            except Exception as e:
                print(f"Scene export failed: {e}")

            # 5. Face Detection
            try:
                zip_data = await fetch_data_as_zip(session, f"{FACE_API_URL}/export", user_id)
                zipf.writestr("face_detection.json", zip_data)
            except Exception as e:
                print(f"Face export failed: {e}")

    buffer.seek(0)
    return buffer.read()
