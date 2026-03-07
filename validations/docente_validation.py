import re
from models.docente_model import Docente

def validate(data: Docente):
    # Validar tipo de documento
    tipos_validos = ['CC', 'TI', 'CE', 'PA', 'RC', 'NIT']
    if data.tipo_documento not in tipos_validos:
        return {"error": "Tipo de documento no válido"}

    # Validar número de documento positivo
    if data.n_documento <= 0:
        return {"error": "Número de documento debe ser positivo"}

    # Validar formato de email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data.email):
        return {"error": "Formato de email no válido"}

    # Validar teléfono (solo dígitos, longitud razonable)
    if not data.telefono.isdigit() or len(data.telefono) < 7 or len(data.telefono) > 15:
        return {"error": "Teléfono debe contener solo dígitos y tener entre 7 y 15 caracteres"}

    # Validar nombres no vacíos
    if not data.primer_nombre.strip():
        return {"error": "Primer nombre es requerido"}

    if not data.primer_apellido.strip():
        return {"error": "Primer apellido es requerido"}

    return {"valid": True}