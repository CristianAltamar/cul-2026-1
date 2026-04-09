from config.db_config import get_db_connection
from controllers.grupo_controller import GrupoController
from controllers.jornada_controller import JornadaController
from models.horario_model import Horario

def validate(data: Horario):
    grupo_controller = GrupoController()
    jornada_controller = JornadaController()

    # Validar que el grupo exista
    try:
        grupo_controller.get_grupo(data.id_grupo)
    except Exception:
        return {"error": "Grupo no existe"}

    # Validar que la jornada exista
    try:
        jornada_controller.get_jornada(data.id_jornada)
    except Exception:
        return {"error": "Jornada no existe"}

    return {"valid": True}