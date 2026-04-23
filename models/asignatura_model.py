from pydantic import BaseModel

class Asignatura(BaseModel):
    id: int = None
    id_programa: int
    nombre: str
    estado: bool