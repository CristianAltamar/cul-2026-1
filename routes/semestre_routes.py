from fastapi import APIRouter, HTTPException
from controllers.periodo_controller import *
from models.periodo_model import Periodo
from validations.periodo_validation import validate

router = APIRouter(tags=["Semestres / Periodos"])

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