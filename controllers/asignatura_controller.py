import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.asignatura_model import Asignatura
from fastapi.encoders import jsonable_encoder
    
class AsignaturaController:
        
    def create_asignatura(self, asignatura: Asignatura):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO asignaturas (id_programa, nombre, estado) VALUES (%s,%s,%s)", (asignatura.id_programa,asignatura.nombre,asignatura.estado))
            conn.commit()
            conn.close()
            return {"resultado": "asignatura creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear asignatura")
        finally:
            conn.close()
        

    def get_asignatura(self, asignatura_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT a.id_asignatura, a.id_programa, p.nombre, a.nombre, a.estado FROM asignaturas a JOIN programas p ON a.id_programa = p.id_programa WHERE a.id_asignatura = %s AND a.estado = true", (asignatura_id,))
            result = cursor.fetchone()

            if result:
                content={
                        'id':int(result[0]),
                        'id_programa':int(result[1]),
                        'programa':result[2],
                        'nombre':result[3],
                        'estado':bool(result[4])
                }
                
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="asignatura not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener asignatura")
        finally:
            conn.close()
    
    def get_asignaturas(self, programa_id: int | None = None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if programa_id is not None:
                cursor.execute(
                    "SELECT a.id_asignatura, a.id_programa, p.nombre, a.nombre, a.estado FROM asignaturas a JOIN programas p ON a.id_programa = p.id_programa WHERE a.estado = true AND a.id_programa = %s",
                    (programa_id,)
                )
            else:
                cursor.execute(
                    "SELECT a.id_asignatura, a.id_programa, p.nombre, a.nombre, a.estado FROM asignaturas a JOIN programas p ON a.id_programa = p.id_programa WHERE a.estado = true"
                )
            result = cursor.fetchall()
            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'id_programa':int(data[1]),
                        'programa':data[2],
                        'nombre':data[3],
                        'estado':bool(data[4])
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)
                return {"resultado": json_data}
            else:
                return {"resultado": []}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener asignaturas")
        finally:
            conn.close()
    
    def update_asignatura(self, asignatura_id: int, asignatura: Asignatura):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE asignaturas SET id_programa = %s, nombre = %s, estado = %s WHERE id_asignatura = %s", (asignatura.id_programa, asignatura.nombre, asignatura.estado, asignatura_id))
            conn.commit()
            conn.close()
            return {"resultado": "asignatura actualizada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar asignatura")
        finally:
            conn.close()
    
    def delete_asignatura(self, asignatura_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE asignaturas SET estado = false WHERE id_asignatura = %s", (asignatura_id,))
            conn.commit()
            conn.close()
            return {"resultado": "asignatura eliminada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar asignatura")
        finally:
            conn.close()