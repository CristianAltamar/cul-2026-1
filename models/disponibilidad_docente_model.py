from pydantic import BaseModel

class DisponibilidadDocente(BaseModel):
    id:int=None
    id_docente:int
    nombre:str|None
    id_periodo:int
    periodo:str|None
    dia_semana:int
    hora_inicio:str
    hora_fin:str
    observacion:str|None