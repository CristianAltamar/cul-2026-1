from fastapi import APIRouter, HTTPException
from controllers.asignatura_controller import *
from models.asignatura_model import Asignatura
from validations.asignatura_validation import validate

router = APIRouter(tags=["Asignaturas"])

nuevo_asignatura = AsignaturaController()


@router.post("/create_asignatura")
async def create_asignatura(asignatura: Asignatura):
    validation = validate(asignatura)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    
    rpta = nuevo_asignatura.create_asignatura(asignatura)
    return rpta


@router.get("/get_asignatura/{asignatura_id}",response_model=Asignatura)
async def get_asignatura(asignatura_id: int):
    rpta = nuevo_asignatura.get_asignatura(asignatura_id)
    return rpta

@router.get("/get_asignaturas/")
async def get_asignaturas():
    rpta = nuevo_asignatura.get_asignaturas()
    return rpta