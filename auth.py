# auth.py
import jwt
import os
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Configuration JWT
JWT_SECRET = os.getenv("JWT_SECRET", "votre_cle_secrete")  # Assurez-vous que cela correspond à Node.js
JWT_ALGORITHM = "HS256"

# Sécurité
security = HTTPBearer(auto_error=False)

def verify_token(token: str) -> dict:
    """
    Vérifie et décode le token JWT.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Extrait et valide l'utilisateur à partir du token JWT. Retourne le user_id.
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Token d'authentification requis")
    
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token sans ID utilisateur")
    
    return str(user_id)

# Middleware d’injection automatique du user_id
async def inject_user_middleware(request: Request, call_next):
    """
    Middleware qui injecte le user_id dans request.state si requis.
    """
    if "/annotation/" in str(request.url):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get("id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sans ID utilisateur")
        
        request.state.user_id = str(user_id)

    return await call_next(request)

# Utilitaire pour extraire user_id manuellement (hors dépendance)
async def extract_user_from_request(request: Request) -> str:
    """
    Extrait manuellement user_id depuis le header Authorization d'une requête.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Token sans ID utilisateur")

    return str(user_id)
