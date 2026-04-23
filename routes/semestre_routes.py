from fastapi import APIRouter, HTTPException
from controllers.periodo_controller import *
from models.periodo_model import Periodo
from validations.periodo_validation import validate

router = APIRouter()

nuevo_periodo = PeriodoController()


@router.post("/create_periodo")
async def create_periodo(periodo: Periodo):
    validation = validate(periodo)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    rpta = nuevo_periodo.create_periodo(periodo)
    return rpta


@router.get("/get_periodo/{periodo_id}",response_model=Periodo)
async def get_periodo(periodo_id: int):
    rpta = nuevo_periodo.get_periodo(periodo_id)
    return rpta

@router.get("/get_periodos/")
async def get_periodos():
    rpta = nuevo_periodo.get_periodos()
    return rpta

@router.put("/update_periodo/{periodo_id}")
async def update_periodo(periodo_id: int, periodo: Periodo):
    rpta = nuevo_periodo.update_periodo(periodo_id, periodo)
    return rpta

@router.delete("/delete_periodo/{periodo_id}")
async def delete_periodo(periodo_id: int):
    rpta = nuevo_periodo.delete_periodo(periodo_id)
    return rpta