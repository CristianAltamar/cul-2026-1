from fastapi import APIRouter, HTTPException
from controllers.grupo_controller import *
from models.grupo_model import Grupo
from validations.grupo_validation import validate

router = APIRouter(tags=["Grupos"])

nuevo_grupo = GrupoController()


@router.post("/create_grupo")
async def create_grupo(grupo: Grupo):
    validation = validate(grupo)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    
    rpta = nuevo_grupo.create_grupo(grupo)
    return rpta


@router.get("/get_grupo/{grupo_id}",response_model=Grupo)
async def get_grupo(grupo_id: int):
    rpta = nuevo_grupo.get_grupo(grupo_id)
    return rpta

@router.get("/get_grupos/")
async def get_grupos():
    rpta = nuevo_grupo.get_grupos()
    return rpta