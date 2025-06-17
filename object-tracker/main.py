from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from db import tracking_col


from tracking_service import process_tracking, get_tracking_results, delete_tracking_results

load_dotenv()

app = FastAPI(title="Tracking Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer les dossiers requis
os.makedirs("videos", exist_ok=True)
os.makedirs("static/tracks", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/track")
async def track_video(
    request: Request,
    video_file: UploadFile = File(...),
    threshold: float = Form(0.6)
):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return await process_tracking(video_file, threshold, user_id)

@app.get("/results")
async def get_track_results(
    request: Request,
    video: str = Query(...)
):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return get_tracking_results(video, user_id)

@app.delete("/results")
async def delete_track_results(
    request: Request,
    video: str = Query(...)
):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return delete_tracking_results(video, user_id)

@app.get("/export")
async def export_tracking(request: Request):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
    results = list(tracking_col.find({"user_id": user_id}, {"_id": 0}))
    return JSONResponse(content=results)
