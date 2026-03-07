import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.docente_model import Docente
from fastapi.encoders import jsonable_encoder
    
class DocenteController:
        
    def create_docente(self, docente: Docente): 
        conn = None  
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO docentes (tipo_documento,numero_documento,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,email,telefono,estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (docente.tipo_documento,docente.n_documento,docente.primer_nombre,docente.segundo_nombre,docente.primer_apellido,docente.segundo_apellido,docente.email,docente.telefono,docente.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Docente creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear docente")
        finally:
            if conn:
                conn.close()
        

    def get_docente(self, docente_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM docentes WHERE id_docente = %s", (docente_id,))
            result = cursor.fetchone()

            if result:
                content={
                        'id':int(result[0]),
                        'tipo_documento':result[1],
                        'n_documento':int(result[2]),
                        'primer_nombre':result[3],
                        'segundo_nombre':result[4],
                        'primer_apellido':result[5],
                        'segundo_apellido':result[6],
                        'email':result[7],
                        'telefono':result[8],
                        'estado':bool(result[9])
                }
                
                json_data = jsonable_encoder(content)            
                return json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="docente not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener docente")
        finally:
            conn.close()
    
    def get_docentes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM docentes")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'tipo_documento':data[1],
                        'n_documento':int(data[2]),
                        'primer_nombre':data[3],
                        'segundo_nombre':data[4],
                        'primer_apellido':data[5],
                        'segundo_apellido':data[6],
                        'email':data[7],
                        'telefono':data[8],
                        'estado':bool(data[9])
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="docente not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener docentes")
        finally:
            conn.close()