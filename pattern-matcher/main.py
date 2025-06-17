# main.py du microservice pattern-matcher
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from matching_service import handle_pattern_matching, retrieve_pattern_matches, delete_pattern_matches

from db import frames_col, matches_col
from pymongo import MongoClient
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from db import matches_col

load_dotenv()
app = FastAPI(title="Pattern Matcher Microservice")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossiers requis
os.makedirs("templates", exist_ok=True)
os.makedirs("videos", exist_ok=True)
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/match")
async def local_match_pattern(
    request: Request,
    video_file: UploadFile = File(...),
    template_file: UploadFile = File(...),
    threshold: float = Form(0.7)
):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return await handle_pattern_matching(video_file, template_file, threshold, user_id)

@app.get("/results")
async def get_results(request: Request, video: str = Query(...), template: str = Query(...)):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return await retrieve_pattern_matches(video, template, user_id)

@app.delete("/results")
async def delete_results(request: Request, video: str = Query(...)):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    return await delete_pattern_matches(video, user_id)


@app.get("/debug/database")
async def debug_database(request: Request):
    user_id = request.headers.get("user_id")
    try:
        total_matches = matches_col.count_documents({})
        user_matches = matches_col.count_documents({"user_id": user_id}) if user_id else 0
        
        sample_docs = list(matches_col.find({}).limit(3))
        
        return {
            "total_documents": total_matches,
            "user_documents": user_matches,
            "sample_documents": sample_docs,
            "user_id": user_id
        }
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/export")
async def export_matching(request: Request):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
    results = list(matches_col.find({"user_id": user_id}, {"_id": 0}))
    return JSONResponse(content=results)
