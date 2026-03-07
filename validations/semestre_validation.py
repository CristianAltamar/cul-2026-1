import re
from datetime import datetime
from models.semestre_model import Semestre

def validate(data: Semestre):
    # Validar nombre no vacío
    if not data.nombre.strip():
        return {"error": "Nombre del semestre es requerido"}

    # Validar formato de fecha (YYYY-MM-DD)
    fecha_regex = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(fecha_regex, data.fecha_inicio):
        return {"error": "Formato de fecha de inicio no válido (debe ser YYYY-MM-DD)"}

    if not re.match(fecha_regex, data.fecha_fin):
        return {"error": "Formato de fecha de fin no válido (debe ser YYYY-MM-DD)"}

    # Validar que las fechas sean válidas
    try:
        fecha_inicio = datetime.strptime(data.fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(data.fecha_fin, '%Y-%m-%d')
    except ValueError:
        return {"error": "Fechas no válidas"}

    # Validar que fecha_inicio < fecha_fin
    if fecha_inicio >= fecha_fin:
        return {"error": "Fecha de inicio debe ser anterior a fecha de fin"}

    return {"valid": True}