from fastapi import APIRouter, HTTPException
from controllers.semestre_controller import *
from models.semestre_model import Semestre
from validations.semestre_validation import validate

router = APIRouter()

nuevo_semestre = SemestreController()


@router.post("/create_semestre")
async def create_semestre(semestre: Semestre):
    validation = validate(semestre)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    rpta = nuevo_semestre.create_semestre(semestre)
    return rpta


@router.get("/get_semestre/{semestre_id}",response_model=Semestre)
async def get_semestre(semestre_id: int):
    rpta = nuevo_semestre.get_semestre(semestre_id)
    return rpta

@router.get("/get_semestres/")
async def get_semestres():
    rpta = nuevo_semestre.get_semestres()
    return rpta