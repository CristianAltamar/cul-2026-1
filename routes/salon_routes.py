from fastapi import APIRouter, HTTPException, Depends
from controllers.salon_controller import *
from middlewares.protected_routes import require_role
from models.salon_model import Salon
from validations.salon_validation import validate

router = APIRouter(tags=["Salones"])

nuevo_salon = SalonController()


@router.post("/create_salon")
async def create_salon(salon: Salon, user = Depends(require_role(1))):
    validation = validate(salon)
    if "error" in validation:
        raise HTTPException(status_code=400, detail=validation["error"])
    rpta = nuevo_salon.create_salon(salon)
    return rpta


@router.get("/get_salon/{salon_id}",response_model=Salon)
async def get_salon(salon_id: int):
    rpta = nuevo_salon.get_salon(salon_id)
    return rpta

@router.get("/get_salones/")
async def get_salones():
    rpta = nuevo_salon.get_salones()
    return rpta

