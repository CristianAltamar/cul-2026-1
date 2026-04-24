import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.horario_model import Horario
from fastapi.encoders import jsonable_encoder
    
class HorarioController:
        
    def create_horario(self, horario: Horario):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO horarios (id_grupo, id_docente, dia_semana, hora_inicio, hora_fin, id_asignatura) VALUES (%s, %s, %s, %s, %s, %s)", (horario.id_grupo, horario.id_docente, horario.dia_semana, horario.hora_inicio, horario.hora_fin, horario.id_asignatura))
            conn.commit()
            conn.close()
            return {"resultado": "horario creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear horario")
        finally:
            conn.close()
        

    def get_horario(self, horario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT h.id_horario, h.id_grupo, g.codigo_grupo, h.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido,  h.id_asignatura, a.nombre, h.dia_semana, h.hora_inicio, h.hora_fin FROM horarios h join grupos g on h.id_grupo = g.id_grupo join docentes d on h.id_docente = d.id_docente join asignaturas a on h.id_asignatura = a.id_asignatura WHERE h.id_horario = %s", (horario_id,))
            result = cursor.fetchone()
            
            if result:
                content={
                        'id':int(result[0]),
                        'id_grupo':int(result[1]),
                        'codigo_grupo':result[2],
                        'id_docente':int(result[3]),
                        'docente':f"{result[4]} {result[5] if result[5] else ''} {result[6]} {result[7] if result[7] else ''}".strip(),
                        'id_asignatura':int(result[8]),
                        'asignatura':result[9],
                        'dia_semana':result[10],
                        'hora_inicio':result[11],
                        'hora_fin':result[12]
                }
                
                json_data = jsonable_encoder(content)            
                return {"resultado": json_data}
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="horario not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener horario")
        finally:
            conn.close()

    def get_horario_docente(self, id_periodo: int, docente_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT h.id_horario, h.id_grupo, g.codigo_grupo, h.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido,  h.id_asignatura, a.nombre, h.dia_semana, h.hora_inicio, h.hora_fin FROM horarios h join grupos g on h.id_grupo = g.id_grupo join docentes d on h.id_docente = d.id_docente join asignaturas a on h.id_asignatura = a.id_asignatura WHERE h.id_periodo = %s AND h.id_docente = %s", (id_periodo, docente_id))
            result = cursor.fetchall()

            if result:
                payload = []
                for data in result:
                    content = {}
                    content={
                            'id':int(data[0]),
                            'id_grupo':int(data[1]),
                            'codigo_grupo':data[2],
                            'id_docente':int(data[3]),
                            'docente':f"{data[4]} {data[5] if data[5] else ''} {data[6]} {data[7] if data[7] else ''}".strip(),
                            'id_asignatura':int(data[8]),
                            'asignatura':data[9],
                            'dia_semana':data[10],
                            'hora_inicio':data[11],
                            'hora_fin':data[12]
                        }
                    payload.append(content)
                json_data = jsonable_encoder(payload)            
                return {"resultado": json_data}
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="horario not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener horario")
        finally:
            conn.close()
    
    def get_horario_programa(self, id_periodo: int, id_programa: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT h.id_horario, h.id_grupo, g.codigo_grupo, h.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido,  h.id_asignatura, a.nombre, h.dia_semana, h.hora_inicio, h.hora_fin FROM horarios h join grupos g on h.id_grupo = g.id_grupo join docentes d on h.id_docente = d.id_docente join asignaturas a on h.id_asignatura = a.id_asignatura join programas p on a.id_programa = p.id_programa WHERE h.id_periodo = %s AND a.id_programa = %s", (id_periodo, id_programa))
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'id_grupo':data[1],
                        'codigo_grupo':data[2],
                        'id_docente':data[3],
                        'docente':f"{data[4]} {data[5] if data[5] else ''} {data[6]} {data[7] if data[7] else ''}".strip(),
                        'id_asignatura':data[8],
                        'asignatura':data[9],
                        'dia_semana':data[12],
                        'hora_inicio':data[13],
                        'hora_fin':data[14]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="horario not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener horarios")
        finally:
            conn.close()
    
    def update_horario(self, horario_id: int, horario: Horario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE horarios SET id_grupo = %s, id_docente = %s, dia_semana = %s, hora_inicio = %s, hora_fin = %s, id_asignatura = %s WHERE id_horario = %s", (horario.id_grupo, horario.id_docente, horario.dia_semana, horario.hora_inicio, horario.hora_fin, horario.id_asignatura, horario_id))
            conn.commit()
            conn.close()
            return {"resultado": "horario actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar horario")
        finally:
            conn.close()
    
    def delete_horario(self, horario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM horarios WHERE id_horario = %s", (horario_id,))
            conn.commit()
            conn.close()
            return {"resultado": "horario eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar horario")
        finally:
            conn.close()