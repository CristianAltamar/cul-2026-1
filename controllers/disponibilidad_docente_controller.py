import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.disponibilidad_docente_model import DisponibilidadDocente
from fastapi.encoders import jsonable_encoder
    
class DisponibilidadDocenteController:
        
    def create_disponibilidad_docente(self, disponibilidadDocente: DisponibilidadDocente):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO disponibilidad_docente (id_docente, id_periodo, dia_semana, hora_inicio, hora_fin, observacion) VALUES (%s, %s, %s, %s, %s, %s)", (disponibilidadDocente.id_docente, disponibilidadDocente.id_periodo, disponibilidadDocente.dia_semana, disponibilidadDocente.hora_inicio, disponibilidadDocente.hora_fin, disponibilidadDocente.observacion))
            conn.commit()
            conn.close()
            return {"resultado": "disponibilidadDocente creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear disponibilidadDocente")
        finally:
            conn.close()
        

    def get_disponibilidad_docente(self, docente_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT dd.id_disponibilidad, dd.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido, dd.id_periodo, p.nombre, dd.dia_semana, dd.hora_inicio, dd.hora_fin, dd.observacion FROM disponibilidad_docente dd join docentes d on dd.id_docente = d.id_docente join periodos p on dd.id_periodo = p.id_periodo WHERE dd.id_docente = %s", (docente_id,))
            result = cursor.fetchall()

            if result:
                payload = []
                content = {}
                for data in result:
                    content={
                            'id':int(data[0]),
                            'id_docente':int(data[1]),
                            'nombre':f"{data[2]} {data[3] if data[3] else ''} {data[4]} {data[5] if data[5] else ''}".strip(),
                            'id_periodo':int(data[6]),
                            'periodo':data[7],
                            'dia_semana':int(data[8]),
                            'hora_inicio':data[9],
                            'hora_fin':data[10],
                            'observacion':data[11]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)
                return json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="disponibilidad docente not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener disponibilidad docente")
        finally:
            conn.close()
    
    def get_disponibilidad_docentes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT dd.id_disponibilidad, dd.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido, dd.id_periodo, p.nombre, dd.dia_semana, dd.hora_inicio, dd.hora_fin, dd.observacion FROM disponibilidad_docente dd join docentes d on dd.id_docente = d.id_docente join periodos p on dd.id_periodo = p.id_periodo")
            result = cursor.fetchall()

            if result:
                payload = []
                content = {} 
                for data in result:
                    content={
                        'id':int(data[0]),
                        'id_docente':int(data[1]),
                        'nombre':f"{data[2]} {data[3] if data[3] else ''} {data[4]} {data[5] if data[5] else ''}".strip(),
                        'id_periodo':int(data[6]),
                        'periodo':data[7],
                        'dia_semana':int(data[8]),
                        'hora_inicio':data[9],
                        'hora_fin':data[10],
                        'observacion':data[11]
                    }
                    payload.append(content)
                    content = {}
                json_data = jsonable_encoder(payload)        
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="disponibilidad docente not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al obtener disponibilidad docentes")
        finally:
            conn.close()