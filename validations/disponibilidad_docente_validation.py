from controllers.docente_controller import DocenteController
from controllers.disponibilidad_docente_controller import DisponibilidadDocenteController
from models.disponibilidad_docente_model import DisponibilidadDocente
from typing import List

docente_controller = DocenteController()
disponibilidad_controller = DisponibilidadDocenteController()

def validate(data: DisponibilidadDocente):
    try:
        docente_controller.get_docente(data.id_docente)
    except Exception:
        return {"error": "Docente no existe"}

    return {"valid": True}


def disponibilidad_exists(data: DisponibilidadDocente) -> bool:
    return bool(disponibilidad_controller.get_disponibilidad_exact(data))


def update_overlapping_disponibilidad(data: DisponibilidadDocente) -> bool:
    overlapping = disponibilidad_controller.get_overlapping_disponibilidad(data)
    if overlapping:
        disponibilidad_id = int(overlapping[0])
        disponibilidad_controller.update_disponibilidad_docente(disponibilidad_id, data)
        return True
    return False


def filter_new_disponibilidad_docentes(disponibilidadDocentes: List[DisponibilidadDocente]) -> List[DisponibilidadDocente]:
    filtered = []
    for disponibilidadDocente in disponibilidadDocentes:
        if disponibilidad_exists(disponibilidadDocente):
            continue
        if update_overlapping_disponibilidad(disponibilidadDocente):
            continue
        filtered.append(disponibilidadDocente)
    return filtered


def validate_multiple_disponibilidad_docentes(disponibilidadDocentes: List[DisponibilidadDocente]):
    for disponibilidadDocente in disponibilidadDocentes:
        validation = validate(disponibilidadDocente)
        if "error" in validation:
            return {"error": validation["error"]}

    new_items = filter_new_disponibilidad_docentes(disponibilidadDocentes)
    return {"valid": True, "new_items": new_items}