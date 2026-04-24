from config.db_config import get_db_connection
from controllers.grupo_controller import GrupoController
from controllers.disponibilidad_docente_controller import DisponibilidadDocenteController
from models.horario_model import Horario

def validate(data: Horario):
    grupo_controller = GrupoController()
    disponibilidad_controller = DisponibilidadDocenteController()

    # Validar que el grupo exista
    try:
        grupo = grupo_controller.get_grupo(data.id_grupo)
    except Exception:
        return {"error": "Grupo no existe"}

    # Validar que el grupo esté en el mismo periodo que el horario
    if grupo['id_periodo'] != data.id_periodo:
        return {"error": "El grupo no pertenece al mismo periodo que el horario"}

    # Validar que el horario esté dentro de la disponibilidad del docente
    if not disponibilidad_controller.check_horario_in_disponibilidad(data.id_docente, data.id_periodo, data.dia_semana, data.hora_inicio, data.hora_fin):
        return {"error": "El horario no está dentro de la disponibilidad del docente"}

    return {"valid": True}