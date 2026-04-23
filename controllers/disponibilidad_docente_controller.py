import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.disponibilidad_docente_model import DisponibilidadDocente
from fastapi.encoders import jsonable_encoder
from typing import List
    
class DisponibilidadDocenteController:
        
    def create_disponibilidad_docente(self, disponibilidadDocente: DisponibilidadDocente):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO disponibilidad_docente (id_docente, id_periodo, dia_semana, hora_inicio, hora_fin, observacion) VALUES (%s, %s, %s, %s, %s, %s)", (disponibilidadDocente.id_docente, disponibilidadDocente.id_periodo, disponibilidadDocente.dia_semana, disponibilidadDocente.hora_inicio, disponibilidadDocente.hora_fin, disponibilidadDocente.observacion))
            conn.commit()
            self.cleanup_disponibilidad(disponibilidadDocente.id_docente, disponibilidadDocente.id_periodo, disponibilidadDocente.dia_semana)
            return {"resultado": "disponibilidadDocente creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear disponibilidadDocente")
        finally:
            conn.close()
        

    def create_multiple_disponibilidad_docente(self, disponibilidadDocentes: List[DisponibilidadDocente], request_items: List[DisponibilidadDocente]):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            values = [(dd.id_docente, dd.id_periodo, dd.dia_semana, dd.hora_inicio, dd.hora_fin, dd.observacion) for dd in disponibilidadDocentes]
            if values:
                cursor.executemany("INSERT INTO disponibilidad_docente (id_docente, id_periodo, dia_semana, hora_inicio, hora_fin, observacion) VALUES (%s, %s, %s, %s, %s, %s)", values)
                conn.commit()

            unique_keys = set((dd.id_docente, dd.id_periodo, dd.dia_semana) for dd in request_items)
            for docente_id, periodo_id, dia_semana in unique_keys:
                current_items = [
                    item for item in request_items
                    if item.id_docente == docente_id and item.id_periodo == periodo_id and item.dia_semana == dia_semana
                ]
                self.cleanup_disponibilidad(docente_id, periodo_id, dia_semana, current_items=current_items)

            return {"resultado": "disponibilidades docentes procesadas"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear disponibilidades docentes")
        finally:
            conn.close()
        

    def cleanup_disponibilidad(self, docente_id: int, periodo_id: int, dia_semana: int, current_items: List[DisponibilidadDocente] = None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_disponibilidad, hora_inicio, hora_fin, observacion FROM disponibilidad_docente WHERE id_docente = %s AND id_periodo = %s AND dia_semana = %s ORDER BY hora_inicio",
                (docente_id, periodo_id, dia_semana),
            )
            rows = cursor.fetchall()

            if not rows:
                return

            if current_items is not None:
                keep_ranges = {(item.hora_inicio, item.hora_fin) for item in current_items}
                delete_ids = [row[0] for row in rows if (str(row[1]), str(row[2])) not in keep_ranges]
                if delete_ids:
                    cursor.execute("DELETE FROM disponibilidad_docente WHERE id_disponibilidad IN %s", (tuple(delete_ids),))
                    rows = [row for row in rows if row[0] not in delete_ids]

                if not rows:
                    conn.commit()
                    return

            merged = []
            for id_disponibilidad, hora_inicio, hora_fin, observacion in rows:
                if not merged or hora_inicio > merged[-1][2]:
                    merged.append([id_disponibilidad, hora_inicio, hora_fin, observacion or ""])
                else:
                    if hora_fin > merged[-1][2]:
                        merged[-1][2] = hora_fin
                    if not merged[-1][3] and observacion:
                        merged[-1][3] = observacion
                    elif observacion and observacion not in merged[-1][3]:
                        merged[-1][3] = f"{merged[-1][3]}; {observacion}" if merged[-1][3] else observacion

            if len(merged) == len(rows) and all(
                merged_i[1] == rows[i][1] and merged_i[2] == rows[i][2] and merged_i[3] == (rows[i][3] or "")
                for i, merged_i in enumerate(merged)
            ):
                conn.commit()
                return

            keep_ids = {segment[0] for segment in merged}
            for id_disponibilidad, hora_inicio, hora_fin, observacion in merged:
                cursor.execute(
                    "UPDATE disponibilidad_docente SET hora_inicio = %s, hora_fin = %s, observacion = %s WHERE id_disponibilidad = %s",
                    (hora_inicio, hora_fin, observacion, id_disponibilidad),
                )

            delete_ids = [row[0] for row in rows if row[0] not in keep_ids]
            if delete_ids:
                cursor.execute("DELETE FROM disponibilidad_docente WHERE id_disponibilidad IN %s", (tuple(delete_ids),))

            conn.commit()
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al limpiar disponibilidades docentes")
        finally:
            conn.close()

    def get_disponibilidad_exact(self, disponibilidadDocente: DisponibilidadDocente):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_disponibilidad FROM disponibilidad_docente WHERE id_docente = %s AND id_periodo = %s AND dia_semana = %s AND hora_inicio = %s AND hora_fin = %s",
                (
                    disponibilidadDocente.id_docente,
                    disponibilidadDocente.id_periodo,
                    disponibilidadDocente.dia_semana,
                    disponibilidadDocente.hora_inicio,
                    disponibilidadDocente.hora_fin,
                ),
            )
            return cursor.fetchone()
        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error al verificar disponibilidad exacta")
        finally:
            conn.close()

    def get_overlapping_disponibilidad(self, disponibilidadDocente: DisponibilidadDocente):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_disponibilidad FROM disponibilidad_docente WHERE id_docente = %s AND id_periodo = %s AND dia_semana = %s AND hora_inicio < %s AND hora_fin > %s",
                (
                    disponibilidadDocente.id_docente,
                    disponibilidadDocente.id_periodo,
                    disponibilidadDocente.dia_semana,
                    disponibilidadDocente.hora_fin,
                    disponibilidadDocente.hora_inicio,
                ),
            )
            return cursor.fetchone()
        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error al verificar disponibilidad superpuesta")
        finally:
            conn.close()

    def update_disponibilidad_docente(self, disponibilidad_id: int, disponibilidadDocente: DisponibilidadDocente):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE disponibilidad_docente SET hora_inicio = %s, hora_fin = %s, observacion = %s WHERE id_disponibilidad = %s",
                (
                    disponibilidadDocente.hora_inicio,
                    disponibilidadDocente.hora_fin,
                    disponibilidadDocente.observacion,
                    disponibilidad_id,
                ),
            )
            conn.commit()
            self.cleanup_disponibilidad(disponibilidadDocente.id_docente, disponibilidadDocente.id_periodo, disponibilidadDocente.dia_semana)
            return {"resultado": "disponibilidadDocente actualizada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar disponibilidad docente")
        finally:
            conn.close()

    def get_disponibilidad_docente(self, docente_id: int, periodo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT dd.id_disponibilidad, dd.id_docente, d.primer_nombre, d.segundo_nombre, d.primer_apellido, d.segundo_apellido, dd.id_periodo, p.nombre, dd.dia_semana, dd.hora_inicio, dd.hora_fin, dd.observacion FROM disponibilidad_docente dd join docentes d on dd.id_docente = d.id_docente join periodos p on dd.id_periodo = p.id_periodo WHERE dd.id_docente = %s AND dd.id_periodo = %s", (docente_id, periodo_id))
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
                return []
                
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
<<<<<<< HEAD
    
    def delete_disponibilidad_docente(self, disponibilidad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM disponibilidad_docente WHERE id_disponibilidad = %s", (disponibilidad_id,))
            conn.commit()
            conn.close()
            return {"resultado": "disponibilidad docente eliminada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar disponibilidad docente")
=======

    def check_horario_in_disponibilidad(self, docente_id: int, periodo_id: int, dia_semana: int, hora_inicio: str, hora_fin: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM disponibilidad_docente WHERE id_docente = %s AND id_periodo = %s AND dia_semana = %s AND hora_inicio <= %s AND hora_fin >= %s",
                (docente_id, periodo_id, dia_semana, hora_inicio, hora_fin)
            )
            result = cursor.fetchone()
            return result[0] > 0
        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error al verificar horario en disponibilidad")
>>>>>>> 9c9527b95fd314a3cea47194b2fff27143d59007
        finally:
            conn.close()