@echo off
REM Active ton environnement virtuel
call venv\Scripts\activate

REM Lancer MongoDB (doit être installé localement)
start "" cmd /k "mongod --dbpath C:\data\db"

REM API Gateway
start cmd /k "cd api-gateway && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Annotation
start cmd /k "cd image-annotator && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

REM Pattern
start cmd /k "cd pattern-matcher && uvicorn main:app --host 0.0.0.0 --port 8002 --reload"

REM Tracking
start cmd /k "cd object-tracker && uvicorn main:app --host 0.0.0.0 --port 8003 --reload"

REM Scene Splitter
start cmd /k "cd video-scene-splitter && uvicorn main:app --host 0.0.0.0 --port 8004 --reload"

REM Face Detector
start cmd /k "cd face-detector && uvicorn main:app --host 0.0.0.0 --port 8005 --reload"

REM Export Service
start cmd /k "cd export && uvicorn main:app --host 0.0.0.0 --port 8006 --reload"

REM Frontend (Node)
start cmd /k "cd front-end && npm run dev"

REM Server (Node)
Start cmd /k "cd authentification && node server.js"

echo Tous les services sont lancés.
pause
