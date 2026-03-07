import re
from models.jornada_model import Jornada

def validate(data: Jornada):
    # Validar nombre no vacío
    if not data.nombre.strip():
        return {"error": "Nombre de jornada es requerido"}

    # Validar formato de hora (HH:MM)
    hora_regex = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    if not re.match(hora_regex, data.hora_inicio):
        return {"error": "Formato de hora de inicio no válido (debe ser HH:MM)"}

    if not re.match(hora_regex, data.hora_fin):
        return {"error": "Formato de hora de fin no válido (debe ser HH:MM)"}

    # Validar que hora_inicio < hora_fin
    if data.hora_inicio >= data.hora_fin:
        return {"error": "Hora de inicio debe ser anterior a hora de fin"}

    return {"valid": True}