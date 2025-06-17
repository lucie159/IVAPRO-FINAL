from pymongo import MongoClient
import os

# MongoDB URI configurable via variable d'environnement
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["video_analysis"]

frames_col = db["frames"]
scenes_col = db["scenes"]
matches_col = db["matches"]  # collection pour stocker les résultats
