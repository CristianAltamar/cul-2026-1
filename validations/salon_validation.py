from models.salon_model import Salon

def validate(data: Salon):
    # Validar código no vacío
    if not data.codigo.strip():
        return {"error": "Código del salón es requerido"}

    # Validar capacidad positiva
    if data.capacidad <= 0:
        return {"error": "Capacidad del salón debe ser mayor a 0"}

    # Validar tipo no vacío
    if not data.tipo.strip():
        return {"error": "Tipo del salón es requerido"}

    # Validar ubicación no vacía
    if not data.ubicacion.strip():
        return {"error": "Ubicación del salón es requerida"}

    return {"valid": True}