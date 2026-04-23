from config.db_config import get_db_connection
from controllers.grupo_controller import GrupoController
from controllers.jornada_controller import JornadaController
<<<<<<< HEAD
from controllers.asignatura_controller import AsignaturaController
=======
from controllers.disponibilidad_docente_controller import DisponibilidadDocenteController
>>>>>>> 9c9527b95fd314a3cea47194b2fff27143d59007
from models.horario_model import Horario

def validate(data: Horario):
    grupo_controller = GrupoController()
    jornada_controller = JornadaController()
<<<<<<< HEAD
    asignatura_controller = AsignaturaController()
=======
    disponibilidad_controller = DisponibilidadDocenteController()
>>>>>>> 9c9527b95fd314a3cea47194b2fff27143d59007

    # Validar que el grupo exista
    try:
        grupo = grupo_controller.get_grupo(data.id_grupo)
    except Exception:
        return {"error": "Grupo no existe"}

    # Validar que la jornada exista
    try:
        jornada = jornada_controller.get_jornada(data.id_jornada)
    except Exception:
        return {"error": "Jornada no existe"}

<<<<<<< HEAD
    # Validar que la asignatura exista
    try:
        asignatura_controller.get_asignatura(data.id_asignatura)
    except Exception:
        return {"error": "Asignatura no existe"}
=======
    # Validar que el grupo esté en el mismo periodo y jornada que el horario
    if grupo['id_periodo'] != data.id_periodo:
        return {"error": "El grupo no pertenece al mismo periodo que el horario"}
    if grupo['id_jornada'] != data.id_jornada:
        return {"error": "El grupo no pertenece a la misma jornada que el horario"}

    # Validar que el horario esté dentro del horario de la jornada
    if data.hora_inicio < jornada['hora_inicio'] or data.hora_fin > jornada['hora_fin']:
        return {"error": "El horario no está dentro del horario de la jornada"}

    # Validar que el horario esté dentro de la disponibilidad del docente
    if not disponibilidad_controller.check_horario_in_disponibilidad(data.id_docente, data.id_periodo, data.dia_semana, data.hora_inicio, data.hora_fin):
        return {"error": "El horario no está dentro de la disponibilidad del docente"}
>>>>>>> 9c9527b95fd314a3cea47194b2fff27143d59007

    return {"valid": True}