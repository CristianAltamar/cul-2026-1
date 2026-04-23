from config.db_config import get_db_connection
from controllers.periodo_controller import PeriodoController
from controllers.jornada_controller import JornadaController
from models.grupo_model import Grupo

def validate(data: Grupo):
    periodo_controller = PeriodoController()
    jornada_controller = JornadaController()

    # Validar que el periodo exista
    try:
        periodo_controller.get_periodo(data.id_periodo)
    except Exception:
        return {"error": "Periodo no existe"}

    # Validar que la jornada exista
    try:
        jornada_controller.get_jornada(data.id_jornada)
    except Exception:
        return {"error": "Jornada no existe"}

    return {"valid": True}