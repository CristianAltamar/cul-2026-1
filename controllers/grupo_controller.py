import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.grupo_model import Grupo
from fastapi.encoders import jsonable_encoder
    
class GrupoController:
        
    def create_grupo(self, grupo: Grupo):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO grupos (id_periodo,id_jornada,codigo_grupo,cupo,estado) VALUES (%s,%s,%s,%s,%s)", (grupo.id_periodo,grupo.id_jornada,grupo.codigo,grupo.cupo,grupo.estado))
            conn.commit()
            conn.close()
            return {"resultado": "grupo creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear grupo")
        finally:
            conn.close()
        

    def get_grupo(self, grupo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT g.id_grupo, g.id_periodo, s.nombre, g.id_jornada, j.nombre, g.codigo_grupo, g.cupo, g.estado FROM grupos g join periodos s on g.id_periodo = s.id_periodo join jornadas j on g.id_jornada = j.id_jornada WHERE id_grupo = %s AND g.estado = true", (grupo_id,))
            result = cursor.fetchone()
            
            if result:
                content={
                        'id':int(result[0]),
                        'id_periodo':int(result[1]),
                        'periodo':result[2],
                        'id_jornada':int(result[3]),
                        'jornada':result[4],
                        'codigo':result[5],
                        'cupo':int(result[6]),
                        'estado':bool(result[7])
                }
                
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="grupo not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener grupo")
        finally:
            conn.close()
    
    def get_grupos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT g.id_grupo, g.id_periodo, s.nombre, g.id_jornada, j.nombre, g.codigo_grupo, g.cupo, g.estado FROM grupos g join periodos s on g.id_periodo = s.id_periodo join jornadas j on g.id_jornada = j.id_jornada WHERE g.estado = true")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'id_periodo':data[1],
                        'periodo':data[2],
                        'id_jornada':data[3],
                        'jornada':data[4],
                        'codigo':data[5],
                        'cupo':int(data[6]),
                        'estado':bool(data[7])
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="grupo not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener grupos")
        finally:
            conn.close()
    
    def update_grupo(self, grupo_id: int, grupo: Grupo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE grupos SET id_periodo = %s, id_jornada = %s, codigo_grupo = %s, cupo = %s, estado = %s WHERE id_grupo = %s", (grupo.id_periodo, grupo.id_jornada, grupo.codigo, grupo.cupo, grupo.estado, grupo_id))
            conn.commit()
            conn.close()
            return {"resultado": "grupo actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar grupo")
        finally:
            conn.close()
    
    def delete_grupo(self, grupo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE grupos SET estado = false WHERE id_grupo = %s", (grupo_id,))
            conn.commit()
            conn.close()
            return {"resultado": "grupo eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar grupo")
        finally:
            conn.close()