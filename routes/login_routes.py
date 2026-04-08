from fastapi import APIRouter, HTTPException
from validations.login_validation import validate
from models.login_model import Login

router = APIRouter(tags=["Autenticación/Login"])

@router.post("/login")
async def login(login:Login):
    validation = validate(login)
    
    if "error" in validation:
        raise HTTPException(status_code=401, detail=validation["error"])
    
    return {
        "access_token": validation["access_token"],
        "token_type": "bearer"
    }