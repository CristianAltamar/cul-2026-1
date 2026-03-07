from models.programa_model import Programa

def validate(data: Programa):
    # Validar nombre no vacío
    if not data.nombre.strip():
        return {"error": "Nombre del programa es requerido"}

    # Validar código no vacío
    if not data.codigo.strip():
        return {"error": "Código del programa es requerido"}

    # Validar longitud del código (ejemplo: entre 3 y 10 caracteres)
    if len(data.codigo) < 3 or len(data.codigo) > 10:
        return {"error": "Código del programa debe tener entre 3 y 10 caracteres"}

    return {"valid": True}