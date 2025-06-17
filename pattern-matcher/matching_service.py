# pattern_matching_service.py

import os
import traceback
from utils import save_file_async
from db import matches_col
from matching_logic import match_template_in_video_frames
from pymongo import MongoClient
from httpx import AsyncClient

VIDEO_SCENE_SPLIT_URL = os.getenv("SCENE_SPLIT_URL", "http://localhost:8004/split")

async def handle_pattern_matching(video_file, template_file, threshold, user_id):
    try:
        # 1. Sauvegarde des fichiers
        video_path = await save_file_async(video_file, "videos")
        template_path = await save_file_async(template_file, "templates")
        print(f"📁 Vidéo sauvegardée : {video_path}")
        print(f"📁 Template sauvegardé : {template_path}")

        video_filename = os.path.basename(video_path)
        template_filename = os.path.basename(template_path)

        # 2. Appel au microservice de découpage
        async with AsyncClient() as client:
            response = await client.post(
                VIDEO_SCENE_SPLIT_URL,
                files={"video_file": open(video_path, "rb")},
                headers={"user_id": user_id}
            )

        if response.status_code != 200:
            raise Exception(f"Erreur découpage : {response.status_code} - {response.text}")

        print("🎬 Découpage terminé")

        # 3. Matching sur les frames extraites
        matches = match_template_in_video_frames(user_id, video_filename, template_path, threshold)

        # 4. Filtrage des correspondances par seuil
        filtered = [m for m in matches if m["match_score"] >= threshold]
        print(f"🔍 {len(filtered)} correspondances >= {threshold}")

        if not filtered:
            return {"message": "Aucune correspondance suffisante détectée."}

        # 5. Sauvegarde MongoDB
        for match in filtered:
            match.update({
                "video": video_filename,
                "template": template_filename,
                "user_id": user_id
            })
            matches_col.insert_one(match)

        return {
            "video": video_filename,
            "template": template_filename,
            "matched_frames": filtered
        }

    except Exception as e:
        print(f"❌ Erreur matching : {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}




async def retrieve_pattern_matches(video_filename: str, template_filename: str, user_id: str):
    try:
        print(f"🔍 [DEBUG] Recherche: video={video_filename}, template={template_filename}, user={user_id}")
        
        # Construction de la requête
        query = {
            "video": video_filename,
            "template": template_filename,  # Note: "template" et non "template_name"
            "user_id": user_id
        }
        print(f"🔍 [DEBUG] Requête MongoDB: {query}")
        
        # Exécution de la requête
        results = list(matches_col.find(query, {"_id": 0}))
        
        print(f"🔍 [DEBUG] Nombre de résultats trouvés: {len(results)}")
        if len(results) > 0:
            print(f"🔍 [DEBUG] Exemple de résultat: {results[0]}")
        
        if not results:
            return {"message": "Aucun résultat trouvé."}

        return results

    except Exception as e:
        print(f"❌ Erreur récupération : {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    
async def delete_pattern_matches(video_filename: str, user_id: str):
    try:
        result = matches_col.delete_many({
            "video": video_filename,
            "user_id": user_id
        })

        return {
            "message": "Résultats supprimés avec succès.",
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        print(f"❌ Erreur suppression : {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}