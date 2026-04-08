from fastapi import APIRouter, HTTPException
from controllers.docente_asignatura_controller import *
from models.docente_asignatura_model import DocenteAsignatura
from validations.docente_asignatura_validation import validate

router = APIRouter(tags=["Docente Asignatura"])

nuevo_docenteAsignatura = DocenteAsignaturaController()


@router.post("/create_docenteAsignatura")
async def create_docenteAsignatura(disponibilidadDocente: DocenteAsignatura):
    validation = validate(disponibilidadDocente)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    
    rpta = nuevo_docenteAsignatura.create_docente_asignatura(disponibilidadDocente)
    return rpta


@router.get("/get_docenteAsignatura/{disponibilidadDocente_id}",response_model=DocenteAsignatura)
async def get_docenteAsignatura(disponibilidadDocente_id: int):
    rpta = nuevo_docenteAsignatura.get_docente_asignatura(disponibilidadDocente_id)
    return rpta

@router.get("/get_docenteAsignaturas/")
async def get_docenteAsignaturas():
    rpta = nuevo_docenteAsignatura.get_docente_asignaturas()
    return rpta