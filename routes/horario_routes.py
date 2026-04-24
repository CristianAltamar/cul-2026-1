from fastapi import APIRouter, HTTPException, Depends
from controllers.horario_controller import *
from models.horario_model import Horario
from middlewares.protected_routes import get_current_user, require_role
from validations.horario_validation import validate

router = APIRouter()

nuevo_horario = HorarioController()


@router.post("/create_horario")
async def create_horario(horario: Horario, user = Depends(require_role(1))):
    validation = validate(horario)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    rpta = nuevo_horario.create_horario(horario)
    return rpta


@router.get("/get_horario/{horario_id}", response_model=Horario)
async def get_horario(horario_id: int):
    rpta = nuevo_horario.get_horario(horario_id)
    return rpta

@router.get("/get_horario_docente/{docente_id}")
async def get_horario_docente(docente_id: int, id_periodo: int, current_user = Depends(get_current_user)):
    if docente_id != current_user["user_id"]:
        if current_user["rol"] != 1:
            raise HTTPException(status_code=403, detail="No autorizado")
    
    rpta = nuevo_horario.get_horario_docente(id_periodo, docente_id)
    return rpta
    
@router.get("/get_horario_programa/{id_programa}")
async def get_horario_programa(id_programa: int, id_periodo: int, current_user = Depends(get_current_user)):
    if current_user["rol"] != 1:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    rpta = nuevo_horario.get_horario_programa(id_periodo, id_programa)
    return rpta

@router.get("/get_horarios/")
async def get_horarios():
    rpta = nuevo_horario.get_horarios()
    return rpta

@router.put("/update_horario/{horario_id}")
async def update_horario(horario_id: int, horario: Horario):
    rpta = nuevo_horario.update_horario(horario_id, horario)
    return rpta

@router.delete("/delete_horario/{horario_id}")
async def delete_horario(horario_id: int):
    rpta = nuevo_horario.delete_horario(horario_id)
    return rpta