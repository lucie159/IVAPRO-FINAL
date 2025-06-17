from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from export_logic import generate_user_export_zip
from io import BytesIO
import os

load_dotenv()

app = FastAPI(title="Exportation Microservice")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/export/all")
async def export_all_user_data(request: Request):
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    try:
        zip_bytes = await generate_user_export_zip(user_id)
        return StreamingResponse(
            BytesIO(zip_bytes),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=export_user_{user_id}.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur pendant l'export : {str(e)}")
