from fastapi import APIRouter, HTTPException
from controllers.facultad_controller import *
from models.facultad_model import Facultad

router = APIRouter()

nuevo_facultad = FacultadController()


@router.post("/create_facultad")
async def create_facultad(facultad: Facultad):
    rpta = nuevo_facultad.create_facultad(facultad)
    return rpta


@router.get("/get_facultad/{facultad_id}",response_model=Facultad)
async def get_facultad(facultad_id: int):
    rpta = nuevo_facultad.get_facultad(facultad_id)
    return rpta

@router.get("/get_facultades/")
async def get_facultades():
    rpta = nuevo_facultad.get_facultades()
    return rpta

@router.put("/update_facultad/{facultad_id}")
async def update_facultad(facultad_id: int, facultad: Facultad):
    rpta = nuevo_facultad.update_facultad(facultad_id, facultad)
    return rpta

@router.delete("/delete_facultad/{facultad_id}")
async def delete_facultad(facultad_id: int):
    rpta = nuevo_facultad.delete_facultad(facultad_id)
    return rpta