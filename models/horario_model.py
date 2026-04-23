from pydantic import BaseModel

class Horario(BaseModel):
    id:int=None
    id_grupo:int
    codigo_grupo:str|None = None
    id_docente:int
    docente:str|None = None
    id_jornada:int
    jornada:str|None = None
    dia_semana:int
    hora_inicio:str
    hora_fin:str
    id_asignatura:int
    asignatura:str|None = None