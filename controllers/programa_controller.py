import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.programa_model import Programa
from fastapi.encoders import jsonable_encoder
    
class ProgramaController:
        
    def create_programa(self, programa: Programa):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO programas (nombre,codigo,id_facultad,estado) VALUES (%s,%s,%s,%s)", (programa.nombre,programa.codigo,programa.id_facultad,programa.estado))
            conn.commit()
            conn.close()
            return {"resultado": "programa creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear programa")
        finally:
            conn.close()
        

    def get_programa(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT p.id_programa,p.nombre,p.codigo,p.id_facultad,f.nombre,p.estado FROM programas p JOIN facultades f ON p.id_facultad = f.id WHERE p.id_programa = %s AND p.estado = true", (programa_id,))
            result = cursor.fetchone()
            
            if result:
                content={
                        'id':int(result[0]),
                        'nombre':result[1],
                        'codigo':result[2],
                        'id_facultad':int(result[3]),
                        'nombre_facultad':result[4],
                        'estado':result[5]
                }
                
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="programa not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener programa")
        finally:
            conn.close()
    
    def get_programas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT p.id_programa,p.nombre,p.codigo,p.id_facultad,f.nombre,p.estado FROM programas p JOIN facultades f ON p.id_facultad = f.id WHERE p.estado = true")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'nombre':data[1],
                        'codigo':data[2],
                        'id_facultad':int(data[3]),
                        'nombre_facultad':data[4],
                        'estado':data[5]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="programa not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener programas")
        finally:
            conn.close()
    
    def update_programa(self, programa_id: int, programa: Programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE programas SET nombre = %s, codigo = %s, id_facultad = %s, estado = %s WHERE id_programa = %s", (programa.nombre, programa.codigo, programa.id_facultad, programa.estado, programa_id))
            conn.commit()
            conn.close()
            return {"resultado": "programa actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar programa")
        finally:
            conn.close()
    
    def delete_programa(self, programa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE programas SET estado = false WHERE id_programa = %s", (programa_id,))
            conn.commit()
            conn.close()
            return {"resultado": "programa eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar programa")
        finally:
            conn.close()