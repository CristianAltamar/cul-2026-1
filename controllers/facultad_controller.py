import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.facultad_model import Facultad
from fastapi.encoders import jsonable_encoder
    
class FacultadController:
        
    def create_facultad(self, facultad: Facultad): 
        conn = None  
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO facultades (nombre) VALUES (%s)", (facultad.nombre,))
            conn.commit()
            conn.close()
            return {"resultado": "facultad creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear facultad")
        finally:
            conn.close()
        

    def get_facultad(self, facultad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facultades WHERE id = %s", (facultad_id,))
            result = cursor.fetchone()

            if result:
                content={
                        'id':int(result[0]),
                        'nombre':result[1]
                }
                
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="facultad not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener facultad")
        finally:
            conn.close()
    
    def get_facultades(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facultades")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'nombre':data[1]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="facultad not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener facultades")
        finally:
            conn.close()
    
    def update_facultad(self, facultad_id: int, facultad: Facultad):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE facultades SET nombre = %s WHERE id = %s", (facultad.nombre, facultad_id))
            conn.commit()
            conn.close()
            return {"resultado": "facultad actualizada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar facultad")
        finally:
            conn.close()
    
    def delete_facultad(self, facultad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM facultades WHERE id = %s", (facultad_id,))
            conn.commit()
            conn.close()
            return {"resultado": "facultad eliminada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar facultad")
        finally:
            conn.close()