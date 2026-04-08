from fastapi import APIRouter, HTTPException
from controllers.programa_controller import *
from models.programa_model import Programa
from validations.programa_validation import validate

router = APIRouter(tags=["Programas"])

nuevo_programa = ProgramaController()


@router.post("/create_programa")
async def create_programa(programa: Programa):
    validation = validate(programa)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    rpta = nuevo_programa.create_programa(programa)
    return rpta


@router.get("/get_programa/{programa_id}",response_model=Programa)
async def get_programa(programa_id: int):
    rpta = nuevo_programa.get_programa(programa_id)
    return rpta

@router.get("/get_programas/")
async def get_programas():
    rpta = nuevo_programa.get_programas()
    return rpta