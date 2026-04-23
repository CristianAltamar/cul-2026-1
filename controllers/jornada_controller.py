import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.jornada_model import Jornada
from fastapi.encoders import jsonable_encoder
    
class JornadaController:
        
    def create_jornada(self, jornada: Jornada):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jornadas (nombre,hora_inicio,hora_fin) VALUES (%s,%s,%s)", (jornada.nombre,jornada.hora_inicio,jornada.hora_fin))
            conn.commit()
            conn.close()
            return {"resultado": "jornada creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear jornada")
        finally:
            conn.close()
        

    def get_jornada(self, jornada_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jornadas WHERE id_jornada = %s", (jornada_id,))
            result = cursor.fetchone()
            
            if result:
                content={
                        'id':int(result[0]),
                        'nombre':result[1],
                        'hora_inicio':result[2],
                        'hora_fin':result[3],
                }
                
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="jornada not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener jornada")
        finally:
            conn.close()
    
    def get_jornadas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jornadas")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'nombre':data[1],
                        'hora_inicio':data[2],
                        'hora_fin':data[3],
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="jornada not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener jornadas")
        finally:
            conn.close()
    
    def update_jornada(self, jornada_id: int, jornada: Jornada):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE jornadas SET nombre = %s, hora_inicio = %s, hora_fin = %s WHERE id_jornada = %s", (jornada.nombre, jornada.hora_inicio, jornada.hora_fin, jornada_id))
            conn.commit()
            conn.close()
            return {"resultado": "jornada actualizada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar jornada")
        finally:
            conn.close()
    
    def delete_jornada(self, jornada_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jornadas WHERE id_jornada = %s", (jornada_id,))
            conn.commit()
            conn.close()
            return {"resultado": "jornada eliminada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar jornada")
        finally:
            conn.close()