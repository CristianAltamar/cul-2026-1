from fastapi import APIRouter, HTTPException
from controllers.disponibilidad_docente_controller import *
from models.disponibilidad_docente_model import DisponibilidadDocente
from validations.disponibilidad_docente_validation import validate, validate_multiple_disponibilidad_docentes
from typing import List

router = APIRouter()

nuevo_disponibilidad_docente = DisponibilidadDocenteController()


@router.post("/create_disponibilidad_docente")
async def create_disponibilidad_docente(disponibilidadDocente: DisponibilidadDocente):
    validation = validate(disponibilidadDocente)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    
    rpta = nuevo_disponibilidad_docente.create_disponibilidad_docente(disponibilidadDocente)
    return rpta

@router.post("/create_multiple_disponibilidad_docente")
async def create_multiple_disponibilidad_docente(disponibilidadDocentes: List[DisponibilidadDocente]):
    validation = validate_multiple_disponibilidad_docentes(disponibilidadDocentes)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])

    if not validation["new_items"]:
        return {"resultado": "No hay disponibilidades nuevas para crear"}
    
    rpta = nuevo_disponibilidad_docente.create_multiple_disponibilidad_docente(validation["new_items"])
    return rpta

@router.get("/get_disponibilidad_docente/{docente_id}")
async def get_disponibilidad_docente(docente_id: int, periodo_id: int):
    rpta = nuevo_disponibilidad_docente.get_disponibilidad_docente(docente_id, periodo_id)
    return rpta

@router.get("/get_disponibilidad_docentes/")
async def get_disponibilidad_docentes():
    rpta = nuevo_disponibilidad_docente.get_disponibilidad_docentes()
    return rpta