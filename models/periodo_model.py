from pydantic import BaseModel

class Periodo(BaseModel):
    id: int = None
    nombre: str
    fecha_inicio: str
    fecha_fin: str