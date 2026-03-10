from pydantic import BaseModel

class Grupo(BaseModel):
    id:int=None
    id_periodo:int
    periodo:str|None
    id_asignatura:int
    asignatura:str|None
    id_jornada:int
    jornada:str|None
    codigo:str
    cupo:int
    estado:bool