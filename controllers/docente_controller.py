import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.docente_model import Docente
from fastapi.encoders import jsonable_encoder
from utility.security import hash_password

class DocenteController:
        
    def create_docente(self, docente: Docente): 
        try:
            #password_hash
            docente.password_hash = hash_password(docente.password_hash)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO docentes (tipo_documento,numero_documento,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,telefono,email,password_hash,id_rol,estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (docente.tipo_documento,docente.n_documento,docente.primer_nombre,docente.segundo_nombre,docente.primer_apellido,docente.segundo_apellido,docente.telefono,docente.email,docente.password_hash,docente.id_rol, docente.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Docente creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear docente")
        finally:
            conn.close()
        

    def get_docente(self, docente_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT d.id_docente, d.tipo_documento,d.numero_documento,d.primer_nombre,d.segundo_nombre,d.primer_apellido,d.segundo_apellido,d.telefono,d.email,d.id_rol, r.nombre, d.estado FROM docentes d join roles r on d.id_rol = r.id_rol WHERE d.id_docente = %s AND d.estado = true", (docente_id,))
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
                    'telefono':result[7],
                    'email':result[8],
                    'id_rol':int(result[9]),
                    'rol':result[10],
                    'estado':bool(result[11])
                }
                
                        
                return content
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

    def get_docente_email(self, email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT d.id_docente, d.tipo_documento,d.numero_documento,d.primer_nombre,d.segundo_nombre,d.primer_apellido,d.segundo_apellido,d.telefono,d.email,d.password_hash,d.id_rol, r.nombre, d.estado FROM docentes d join roles r on d.id_rol = r.id_rol WHERE d.email = %s AND d.estado = true", (email,))
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
                    'telefono':result[7],
                    'email':result[8],
                    'password_hash':result[9],
                    'id_rol':int(result[10]),
                    'rol':result[11],
                    'estado':bool(result[12])
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
            cursor.execute("SELECT d.id_docente, d.tipo_documento,d.numero_documento,d.primer_nombre,d.segundo_nombre,d.primer_apellido,d.segundo_apellido,d.telefono,d.email,d.id_rol, r.nombre, d.estado FROM docentes d join roles r on d.id_rol = r.id_rol WHERE d.estado = true")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':int(data[0]),
                        'tipo_documento':data[1],
                        'n_documento':int(data[2]),
                        'primer_nombre':data[3],
                        'segundo_nombre':data[4],
                        'primer_apellido':data[5],
                        'segundo_apellido':data[6],
                        'telefono':data[7],
                        'email':data[8],
                        'id_rol':int(data[9]),
                        'rol':data[10],
                        'estado':bool(data[11])
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
    
    def update_docente(self, docente_id: int, docente: Docente):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE docentes SET tipo_documento = %s, numero_documento = %s, primer_nombre = %s, segundo_nombre = %s, primer_apellido = %s, segundo_apellido = %s, telefono = %s, email = %s, id_rol = %s, estado = %s WHERE id_docente = %s", (docente.tipo_documento, docente.n_documento, docente.primer_nombre, docente.segundo_nombre, docente.primer_apellido, docente.segundo_apellido, docente.telefono, docente.email, docente.id_rol, docente.estado, docente_id))
            conn.commit()
            conn.close()
            return {"resultado": "docente actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar docente")
        finally:
            conn.close()
    
    def delete_docente(self, docente_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE docentes SET estado = false WHERE id_docente = %s", (docente_id,))
            conn.commit()
            conn.close()
            return {"resultado": "docente eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar docente")
        finally:
            conn.close()