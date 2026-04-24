from pydantic import BaseModel

class Asignatura(BaseModel):
    id: int | None = None
    id_programa: int
    programa: str | None = None
    nombre: str
    estado: bool