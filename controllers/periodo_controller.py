import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.periodo_model import Periodo
from fastapi.encoders import jsonable_encoder
    
class PeriodoController:
        
    def create_periodo(self, periodo: Periodo):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO periodos (nombre,fecha_inicio,fecha_fin) VALUES (%s,%s,%s)", (periodo.nombre,periodo.fecha_inicio,periodo.fecha_fin))
            conn.commit()
            conn.close()
            return {"resultado": "Periodos creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear periodos")
        finally:
            conn.close()
        

    def get_periodo(self, periodo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM periodos WHERE id_periodo = %s", (periodo_id,))
            result = cursor.fetchone()
            
            if result:
                content={
                        'id':int(result[0]),
                        'nombre':result[1],
                        'fecha_inicio':result[2],
                        'fecha_fin':result[3],
                }
                
                json_data = jsonable_encoder(content)            
                return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="Periodos not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener Periodos")
        finally:
            conn.close()
    
    def get_periodos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM periodos")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':data[0],
                        'nombre':data[1],
                        'fecha_inicio':data[2],
                        'fecha_fin':data[3],
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Periodos not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener Periodoss")
        finally:
            conn.close()
    
    def update_periodo(self, periodo_id: int, periodo: Periodo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE periodos SET nombre = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_periodo = %s", (periodo.nombre, periodo.fecha_inicio, periodo.fecha_fin, periodo_id))
            conn.commit()
            conn.close()
            return {"resultado": "periodo actualizado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar periodo")
        finally:
            conn.close()
    
    def delete_periodo(self, periodo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM periodos WHERE id_periodo = %s", (periodo_id,))
            conn.commit()
            conn.close()
            return {"resultado": "periodo eliminado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar periodo")
        finally:
            conn.close()