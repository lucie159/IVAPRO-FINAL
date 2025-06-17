from fastapi import FastAPI
from routers.annotation_router import router as annotation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:3000"] pour React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter ici tous les routers des services

app.include_router(annotation_router)
