import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.docente_asignatura_model import DocenteAsignatura
from fastapi.encoders import jsonable_encoder
    
class DocenteAsignaturaController:
        
    def create_docente_asignatura(self, docenteAsignatura: DocenteAsignatura):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO docente_asignatura (id_docente, id_asignatura) VALUES (%s,%s)", (docenteAsignatura.id_docente,docenteAsignatura.id_asignatura))
            conn.commit()
            conn.close()
            return {"resultado": "docente asignatura creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear docente asignatura")
        finally:
            conn.close()
        

    def get_docente_asignatura(self, docenteAsignatura_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT da.id, da.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido, da.id_asignatura, a.nombre FROM docente_asignatura da JOIN docentes d ON da.id_docente = d.id_docente JOIN asignaturas a ON da.id_asignatura = a.id_asignatura WHERE da.id = %s", (docenteAsignatura_id,))
            result = cursor.fetchone()

            if result:
                content={
                        'id':int(result[0]),
                        'id_docente':int(result[1]),
                        'nombre_docente':f"{result[2]} {result[3] if result[3] else ''} {result[4]} {result[5] if result[5] else ''}".strip(),
                        'id_asignatura':int(result[6]),
                        'nombre_asignatura':result[7]
                }
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="docenteAsignatura not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener docenteAsignatura")
        finally:
            conn.close()
    
    def get_docente_asignaturas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT da.id, da.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido, da.id_asignatura, a.nombre FROM docente_asignatura da JOIN docentes d ON da.id_docente = d.id_docente JOIN asignaturas a ON da.id_asignatura = a.id_asignatura")
            result = cursor.fetchall()
            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':int(data[0]),
                        'id_docente':int(data[1]),
                        'nombre_docente':f"{data[2]} {data[3] if data[3] else ''} {data[4]} {data[5] if data[5] else ''}".strip(),
                        'id_asignatura':int(data[6]),
                        'nombre_asignatura':data[7]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="docenteAsignatura not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    
    def update_docente_asignatura(self, docente_asignatura_id: int, docenteAsignatura: DocenteAsignatura):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE docente_asignatura SET id_docente = %s, id_asignatura = %s WHERE id = %s", (docenteAsignatura.id_docente, docenteAsignatura.id_asignatura, docente_asignatura_id))
            conn.commit()
            conn.close()
            return {"resultado": "docente asignatura actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar docente asignatura")
        finally:
            conn.close()
    
    def delete_docente_asignatura(self, docente_asignatura_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM docente_asignatura WHERE id = %s", (docente_asignatura_id,))
            conn.commit()
            conn.close()
            return {"resultado": "docente asignatura eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar docente asignatura")
        finally:
            conn.close()