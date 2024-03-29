# Modelos de base de datos

##########################################################################################
#Funciones UserModel: get_user, load_users, register_user, check_password, delete_user
#Funciones FabricaModel: add_fabrica, get_fabrica, get_costes_beneficios,
#Funciones RecursosModel: get_humanos_fabrica, get_maquinas_fabrica, get_habilidades_maquina
#                         get_habilidades_trabajadores, obtener_habilidades_recursos, add_maquina
#                         add_trabajador
#Funciones TareaModel: get_soft_skills, get_hard_skills, get_habilidades_subtareas, 
#                      obtener_skills_chatGPT, add_subtask, skills_matching???
#
##########################################################################################
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mysqldb import MySQL
import json
from app import app
from flask import jsonify
import requests
from openai import OpenAI
from config import config

conexion = MySQL(app)

def get_db_connection():
    try:
        conn = conexion.connection
        # Intenta realizar una consulta simple para verificar la conexión
        conn.ping()
    except Exception as e:
        app.logger.error(f'Error al conectar con la base de datos: {e}')
        conn = conexion.connect  # Reconectar si hay un fallo
    return conn

class UserModel(UserMixin):

    def __init__(self, username, name=None, surname=None, password=None):
        self.id = username
        self.name = name
        self.surname = surname
        self.password = generate_password_hash(password) if password else None

    @staticmethod
    def get_user(username):
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT id, nombre, apellidos, username FROM usuarios WHERE username = '{0}'".format(username)
            cursor.execute(sql)
            datos = cursor.fetchone()
            
            if datos != None:
                user = {'id': datos[0], 'nombre': datos[1], 'apellidos': datos[2], 'username': datos[3]}                
                return user
            else:
                return None
        except Exception as ex:
            app.logger.error(f'Error al cargar usuario: {ex}')
            return []

    @staticmethod
    def load_users():
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT nombre, apellidos, username FROM usuarios"
            cursor.execute(sql)
            datos = cursor.fetchall()
            users = [{'nombre': fila[0], 'apellidos': fila[1], 'username': fila[2]} for fila in datos]
            return users
        except Exception as ex:
            app.logger.error(f'Error al cargar usuarios: {ex}')
            return []
    @staticmethod
    def register_user(user):
        try:
            cursor = get_db_connection().cursor()
            sql = "INSERT INTO usuarios (nombre, apellidos, username, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user.name, user.surname, user.id, user.password))
            conexion.connection.commit()
            return user
        except Exception as ex:
            print(f"Error al insertar en la base de datos: {ex}")
            return None

    @staticmethod
    def delete_user(username):
        try:
            cursor = get_db_connection().cursor()
            sql = "DELETE FROM usuarios WHERE username = %s"
            cursor.execute(sql, (username))
            conexion.connection.commit()
            print("Usuario eliminado exitosamente")
        except Exception as ex:
            print(f"Error al eliminar usuario de la base de datos: {ex}")


    def check_password(self, password):
        return check_password_hash(self.password, password)

class FabricaModel:
    @staticmethod
    def add_fabrica(nombre, id_usuario):
        try:
            cursor = get_db_connection().cursor()
            sql =  "INSERT INTO Fabrica (nombre, usuario_id) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, id_usuario))
            conexion.connection.commit()
            return nombre  # Retorna el ID de la nueva fábrica
        except Exception as ex:
            print(f"Error al añadir fábrica: {ex}")
            return None
    
    @staticmethod
    def get_fabrica(id_usuario):
        try:
            cursor = get_db_connection().cursor()
            sql =  "SELECT nombre, costes, beneficios FROM Fabrica WHERE usuario_id = %s"
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
        except Exception as ex:
            print(f"Error al obtener fábricas: {ex}")
            return []
    
    @staticmethod
    def get_costes_beneficios(id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT costes, beneficios FROM Fabrica WHERE id = %s"
            cursor.execute(sql,(id_fabrica,))
            return cursor.fetchone()
        except Exception as ex:
            print(f"Error al sacar costes y beneficios: {ex}")
            return[]
    
    @staticmethod
    def delete_fabrica(id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "DELETE FROM Fabrica WHERE id = %s"
            cursor.execute(sql, (id_fabrica))
            conexion.connection.commit()
            print("Fabrica eliminada exitosamente")
        except Exception as ex:
            print(f"Error al eliminar fabrica de la base de datos: {ex}")

    @staticmethod
    def update_fabrica(fabrica_id, nombre=None, nuevos_costes=None, nuevos_beneficios=None):
        try:
            cursor = get_db_connection().cursor()
            sql = "UPDATE Fabrica SET "
            update_values = []
            if nombre is not None:
                sql += "nombre = %s,"
                update_values.append(nombre)
            if nuevos_costes is not None:
                sql += "costes = %s, "
                update_values.append(nuevos_costes)
            if nuevos_beneficios is not None:
                sql += "beneficios = %s, "
                update_values.append(nuevos_beneficios)
            sql = sql.rstrip(", ") + " WHERE id = %s"  # Usar el ID en lugar del nombre
            update_values.append(fabrica_id)  # Agregar el ID como último valor

            if len(update_values) > 1:  # Verificar si se proporcionaron valores para actualizar
                cursor.execute(sql, tuple(update_values))
                conexion.connection.commit()
                print("Información de la fábrica actualizada exitosamente")
            else:
                print("No se proporcionaron valores para actualizar")
        except Exception as ex:
            print(f"Error al actualizar información de la fábrica: {ex}")

class RecursosModel:
    @staticmethod
    def get_humanos_fabrica(id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT id,codigo FROM Trabajadores WHERE fabrica_id = %s"
            cursor.execute(sql, (id_fabrica,))
            return cursor.fetchall()
        except Exception as ex:
            print(f"Error al obtener los IDs de los trabajadores: {ex}")
            return []

    @staticmethod
    def get_maquinas_farbica(id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT id, codigo FROM Maquinas WHERE fabrica_id = %s"
            cursor.execute(sql, (id_fabrica,))
            return cursor.fetchall()
        except Exception as ex:
            print(f"Error al obtener los IDs de las máquinas: {ex}")
            return []

    @staticmethod
    def add_maquina(id_fabrica, nombre, fatiga, coste_uso, habilidades):
        try:
            cursor = get_db_connection().cursor()
            sql = "INSERT INTO Maquinas (nombre, fatiga, coste, fabrica_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, fatiga, coste_uso, id_fabrica))
            id_maquina = cursor.lastrowid
            for habilidad in habilidades:
                sql_h = ''' INSERT INTO skills_maquinas (maquina_id, skill_id) VALUES (%s,%s)'''
                cursor.execute(sql_h, (id_maquina, habilidad))
            conexion.connection.commit()
            return id_fabrica
        except Exception as ex:
            print(f"Error al insertar en la base de datos: {ex}")
            return None
        
    @staticmethod
    def add_trabajador(id_fabrica, nombre, apellidos, fecha_n, fatiga, coste_uso, preferencia, habilidades):
        try:
            cursor = get_db_connection().cursor()
            sql = '''INSERT INTO Trabajadores (nombre, apellidos, fecha_nacimiento, fatiga, coste_h, preferencias_trabajo, fabrica_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (nombre, apellidos, fecha_n, fatiga, coste_uso, preferencia, id_fabrica))
            id_trabajador = cursor.lastrowid
            for habilidad in habilidades:
                sql_h = '''INSERT INTO skills_trabajadores (trabajador_id, skill_id) VALUES (%s,%s)'''
                cursor.execute(sql_h, (id_trabajador, habilidad))
            conexion.connection.commit()
            return id_trabajador
        except Exception as ex:
            print(f"Error al insertar en la base de datos: {ex}")
            return None

    
    @staticmethod
    def delete_trabajador(codigo_trabajador, id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "DELETE FROM Trabajadores WHERE fabrica_id = %s AND codigo = %s"
            cursor.execute(sql, (id_fabrica, codigo_trabajador))
            conexion.connection.commit()
            print("Trabajador eliminada exitosamente")
        except Exception as ex:
            print(f"Error al eliminar trabajador de la base de datos: {ex}")

    @staticmethod
    def update_trabajador(trabajador_id, nombre=None, apellidos=None, fecha_nacimiento=None, trabajos_apto=None, fatiga=None, coste_h=None, preferencias_trabajo=None, nuevas_habilidades=None):
        try:
            cursor = get_db_connection().cursor()
            update_values_trabajador = []

            if nombre is not None:
                update_values_trabajador.append(('nombre', nombre))
            if apellidos is not None:
                update_values_trabajador.append(('apellidos', apellidos))
            if fecha_nacimiento is not None:
                update_values_trabajador.append(('fecha_nacimiento', fecha_nacimiento))
            if trabajos_apto is not None:
                update_values_trabajador.append(('trabajos_apto', trabajos_apto))
            if fatiga is not None:
                update_values_trabajador.append(('fatiga', fatiga))
            if coste_h is not None:
                update_values_trabajador.append(('coste_h', coste_h))
            if preferencias_trabajo is not None:
                update_values_trabajador.append(('preferencias_trabajo', preferencias_trabajo))

            # Actualizar tabla Trabajador
            if update_values_trabajador:
                sql_trabajador = "UPDATE Trabajador SET " + ", ".join([f"{field} = %s" for field, _ in update_values_trabajador]) + " WHERE id = %s"
                values_trabajador = [value for _, value in update_values_trabajador]
                values_trabajador.append(trabajador_id)
                cursor.execute(sql_trabajador, tuple(values_trabajador))

            # Actualizar habilidades del trabajador
            if nuevas_habilidades is not None:
                # Eliminar habilidades existentes del trabajador
                cursor.execute("DELETE FROM skills_trabajadores WHERE trabajador_id = %s", (trabajador_id,))
                # Insertar nuevas habilidades
                for skill_id in nuevas_habilidades:
                    cursor.execute("INSERT INTO skills_trabajadores (trabajador_id, skill_id) VALUES (%s, %s)", (trabajador_id, skill_id))

            conexion.connection.commit()
            print("Información del trabajador actualizada exitosamente")
        except Exception as ex:
            print(f"Error al actualizar información del trabajador: {ex}")


    @staticmethod
    def delete_maquina(codigo_maquina, id_fabrica):
        try:
            cursor = get_db_connection().cursor()
            sql = "DELETE FROM Maquinas WHERE fabrica_id = %s AND codigo = %s"
            cursor.execute(sql, (id_fabrica, codigo_maquina))
            conexion.connection.commit()
            print("Máquina eliminada exitosamente")
        except Exception as ex:
            print(f"Error al eliminar máquina de la base de datos: {ex}")

    @staticmethod
    def update_maquina(maquina_id, nombre=None, fatiga=None, coste_h=None, habilidades=None):
        try:
            cursor = get_db_connection().cursor()
            update_values_maquina = []
            update_values_habilidades = []

            if nombre is not None:
                update_values_maquina.append(('nombre', nombre))
            if fatiga is not None:
                update_values_maquina.append(('fatiga', fatiga))
            if coste_h is not None:
                update_values_maquina.append(('coste_h', coste_h))

            # Actualizar tabla Maquina
            if update_values_maquina:
                sql_maquina = "UPDATE Maquinas SET " + ", ".join([f"{field} = %s" for field, _ in update_values_maquina]) + " WHERE id = %s"
                values_maquina = [value for _, value in update_values_maquina]
                values_maquina.append(maquina_id)
                cursor.execute(sql_maquina, tuple(values_maquina))

            # Actualizar tabla skills_maquinas
            if habilidades is not None:
                # Eliminar habilidades existentes de la máquina
                cursor.execute("DELETE FROM skills_maquinas WHERE maquina_id = %s", (maquina_id,))
                # Insertar nuevas habilidades
                for skill_id in habilidades:
                    cursor.execute("INSERT INTO skills_maquinas (maquina_id, skill_id) VALUES (%s, %s)", (maquina_id, skill_id))

            conexion.connection.commit()
            print("Información de la máquina actualizada exitosamente")
        except Exception as ex:
            print(f"Error al actualizar información de la máquina: {ex}")

    @staticmethod
    def get_habilidades_maquinas(id_fabrica):
        habilidades_maquinas = {}

        try:
            cursor = get_db_connection().cursor()
            sql = '''SELECT m.codigo, GROUP_CONCAT(IF(s.tipo = 'soft', s.nombre, NULL)) AS soft_skills, 
                        GROUP_CONCAT(IF(s.tipo = 'hard', s.nombre, NULL)) AS technical_skills 
                FROM Maquinas m 
                LEFT JOIN skills_maquinas sm ON m.id = sm.maquina_id 
                LEFT JOIN skills s ON sm.skill_id = s.id 
                WHERE m.fabrica_id = %s 
                GROUP BY m.codigo'''
            cursor.execute(sql, (id_fabrica,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                codigo_maquina = resultado[0]
                soft_skills = resultado[1].split(',') if resultado[1] else []
                technical_skills = resultado[2].split(',') if resultado[2] else []
                habilidades_maquinas[codigo_maquina] = {"soft_skills": soft_skills, "technical_skills": technical_skills}
            return habilidades_maquinas

        except Exception as ex:
            print(f"Error al obtener las habilidades de las máquinas: {ex}")
            return {}
    
    @staticmethod
    def get_habilidades_trabajadores(fabrica_id):
        try:
            cursor = get_db_connection().cursor()
            sql = '''SELECT t.codigo, 
                            GROUP_CONCAT(IF(s.tipo = 'soft', s.nombre, NULL)) AS soft_skills, 
                            GROUP_CONCAT(IF(s.tipo = 'hard', s.nombre, NULL)) AS technical_skills 
                    FROM Trabajadores t 
                    LEFT JOIN skills_trabajadores st ON t.id = st.trabajador_id 
                    LEFT JOIN skills s ON st.skill_id = s.id 
                    WHERE t.fabrica_id = %s 
                    GROUP BY t.codigo'''
            cursor.execute(sql, (fabrica_id,))
            habilidades_trabajadores = {}
            for codigo, soft_skills, technical_skills in cursor.fetchall():
                habilidades_trabajadores[codigo] = {
                    'soft_skills': soft_skills.split(',') if soft_skills else [],
                    'technical_skills': technical_skills.split(',') if technical_skills else []
                }
            return habilidades_trabajadores
        except Exception as ex:
            print(f"Error al obtener habilidades de trabajadores: {ex}")
            return {}
    @staticmethod
    def obtener_habilidades_recursos(fabrica_id):
        h_t = RecursosModel.obtener_habilidades_trabajadores(fabrica_id)
        h_m = RecursosModel.obtener_habilidades_maquinas(fabrica_id)
        h_t.update(h_m)

    @staticmethod
    def calcular_fatiga_total(asignacion):
        try:
            cursor = get_db_connection().cursor()

            # Calcular la fatiga total de la asignación de tareas
            fatiga_total = 0

            for tarea, identificador in asignacion:
                # Determinar si el identificador pertenece a un trabajador o a una máquina
                tipo = identificador[0]  # Primer carácter indica el tipo (H para trabajador, M para máquina)
                if tipo == 'H':
                    tabla = 'Trabajadores'  
                elif tipo == 'M':
                    tabla = 'Maquinas'
                # Consultar la fatiga del trabajador asignado a la tarea en la base de datos
                sql = f"SELECT fatiga FROM {tabla} WHERE id = %s"
                cursor.execute(sql, (identificador,))
                recurso_fatiga = cursor.fetchone()

                if recurso_fatiga:
                    fatiga_total += recurso_fatiga[0]

            return fatiga_total
        except Exception as ex:
            print(f"Error al calcular la fatiga total: {ex}")
            return None

    @staticmethod
    def calcular_coste_total(asignacion):
        try:
            cursor = get_db_connection().cursor()

            # Calcular el coste total de la asignación de tareas
            coste_total = 0

            for tarea, identificador in asignacion:
                # Determinar si el identificador pertenece a un trabajador o a una máquina
                tipo = identificador[0]  # Primer carácter indica el tipo (H para trabajador, M para máquina)

                if tipo == 'H':
                    tabla = 'Trabajadores'  
                elif tipo == 'M':
                    tabla = 'Maquinas'

                # Consultar el coste del trabajador o máquina en la base de datos
                sql = f"SELECT coste_h FROM {tabla} WHERE codigo = %s"
                cursor.execute(sql, (identificador,))
                resultado = cursor.fetchone()

                if resultado:
                    coste_total += resultado[0]

            return coste_total
        except Exception as ex:
            print(f"Error al calcular el coste total: {ex}")
            return None


class TareaModel:
    @staticmethod
    def get_soft_skills():
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT nombre from skills WHERE tipo ='soft'"
            cursor.execute(sql)
            soft_skills = cursor.fetchall()
            return [skill[0] for skill in soft_skills]
        except Exception as ex:
            print(f"Error al obtener las soft skills: {ex}")
            return[]
        
    @staticmethod
    def get_hard_skills(sector):
        try:
            cursor = get_db_connection().cursor()
            sql = "SELECT nombre FROM skills WHERE tipo = 'hard' AND sector = %s"
            cursor.execute(sql,(sector,))
            hard_skills = cursor.fetchall()
            return [skill[0] for skill in hard_skills]
        except Exception as ex:
            print(f"Error al obtener las hard skills: {ex}")
            return[]
    
    @staticmethod
    def get_habilidades_subtareas(fabrica_id):
        try:
            cursor = get_db_connection().cursor()
            sql = '''SELECT s.id, 
                        GROUP_CONCAT(IF(sk.tipo = 'soft', sk.nombre, NULL)) AS soft_skills, 
                        GROUP_CONCAT(IF(sk.tipo = 'hard', sk.nombre, NULL)) AS technical_skills 
                    FROM Subtasks s 
                    LEFT JOIN skills_subtasks ss ON s.id = ss.subtask_id 
                    LEFT JOIN skills sk ON ss.skill_id = sk.id 
                    WHERE s.id = %s 
                    GROUP BY s.id'''
            cursor.execute(sql, (fabrica_id,))
            habilidades_subtareas = {}
            for codigo, soft_skills, technical_skills in cursor.fetchall():
                habilidades_subtareas[codigo] = {
                    'soft_skills': soft_skills.split(',') if soft_skills else [],
                    'technical_skills': technical_skills.split(',') if technical_skills else []
                }
            return habilidades_subtareas
        except Exception as ex:
            print(f"Error al obtener habilidades de subtareas: {ex}")
            return {}


    @staticmethod
    def obtener_skills_chatGPT(sector,descripcion):
        soft_skills = TareaModel.get_soft_skills()
        hard_skills = TareaModel.get_hard_skills(sector)
        configuracion_desarrollo = config['development']()
        prompt = f'''El formato que quiero que me devuelvas la respuesta es el siguiente, donde la X representa un placeholder:
soft_skills = [X], hard_skills = [X]

Dado un listado de habilidades como este: = soft_skills {soft_skills} y hard_skills {hard_skills}, y una descripcion de una tarea:{descripcion}, quiero que me devuelvas una lista SOLO con las habilidades proporcionadas que mejor se ajusten para la tarea.
Por favor, devuélveme la respuesta siguiendo el formato: soft_skills = [X], hard_skills = [X].'''
        url = "https://api.openai.com/v1/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + configuracion_desarrollo.CHATGPT_API_KEY
        }
        data = {
            "prompt": prompt,
            "max_tokens": 300,
            "model": "gpt-3.5-turbo"
        }

        response = requests.post(url, headers=headers, json=data)
        respuesta_json = response.json()

        print(respuesta_json)  # Imprime la respuesta JSON en la consola para ver los datos
        habilidades = []
        if 'choices' in respuesta_json and len(respuesta_json['choices']) > 0:
            for choice in respuesta_json['choices']:
                habilidades.extend(choice['text'].split(','))

        print(habilidades)  # Imprime la respuesta JSON en la consola para ver los datos
        
        # Devuelve la respuesta JSON como salida de la ruta
        return habilidades
    
    @staticmethod
    def add_subtask(nombre, duracion, beneficio, descripcion, fabrica_id):
        # guardar los datos en la base de datos
        # se debe rellenar la tabla de skills_subtaks, tiendo en cuenta la tarea a la que estamos 
        # haciendo referencia y además buscar las habilidades que tocan en la tabla de skills
        
        try:
            cursor = get_db_connection().cursor()
            ### parte tabla de subtasks
            sql = '''INSERT INTO Subtasks(nombre, duracion, beneficio, descripcion, fabrica_id) VALUES(%s, %s, %s, %s, %s)'''
            cursor.execute(sql, (nombre, duracion, beneficio, descripcion, fabrica_id))
            #parte tabla skills_subtasks
            sector = "robotica colaborativa"
            habilidades = TareaModel.obtener_skills_chatGPT(sector, descripcion)
            id_subtask = cursor.lastrowid
            for habilidad in habilidades:
                sql_h = ''' INSERT INTO skills_subtasks (subtask_id, skill_id) VALUES (%s,%s)'''
                cursor.execute(sql_h, (id_subtask, habilidad))
            conexion.connection.commit()
            return fabrica_id
        except Exception as ex:
            print(f"Error al insertar subtarea en la base de datos: {ex}")
            return {}
    
    @staticmethod
    def update_subtask(fabrica_id, subtask_id, nombre=None, duracion=None, beneficio=None, descripcion=None,  nuevas_habilidades=None):
        try:
            cursor = get_db_connection().cursor()
            update_values_subtask = []

            if nombre is not None:
                update_values_subtask.append(('nombre', nombre))
            if duracion is not None:
                update_values_subtask.append(('duracion', duracion))
            if beneficio is not None:
                update_values_subtask.append(('beneficio', beneficio))
            if descripcion is not None:
                update_values_subtask.append(('descripcion', descripcion))

            # Actualizar tabla Subtask
            if update_values_subtask:
                sql_subtask = "UPDATE Subtasks SET " + ", ".join([f"{field} = %s" for field, _ in update_values_subtask]) + " WHERE id = %s AND fabrica_id = %s"
                values_subtask = [value for _, value in update_values_subtask]
                values_subtask.append(subtask_id)
                values_subtask.append(fabrica_id)
                cursor.execute(sql_subtask, tuple(values_subtask))
            if nuevas_habilidades is not None:
                # Eliminar habilidades existentes de la subtask
                cursor.execute("DELETE FROM skills_subtasks WHERE subtask_id = %s", (subtask_id,))
                # Insertar nuevas habilidades
                for skill_id in nuevas_habilidades:
                    cursor.execute("INSERT INTO skills_subtasks (subtask_id, skill_id) VALUES (%s, %s)", (subtask_id, skill_id))

            conexion.connection.commit()
            print("Información de la subtask actualizada exitosamente")
        except Exception as ex:
            print(f"Error al actualizar información de la subtask: {ex}")
    
    @staticmethod
    def calcular_beneficio_total(asignacion):
        try:
            cursor = get_db_connection().cursor()

            # Calcular el coste total de la asignación de tareas
            beneficio_total = 0

            for tarea, identificador in asignacion:

                # Consultar el coste del trabajador o máquina en la base de datos
                sql = f"SELECT beneficio FROM Subtasks WHERE codigo = %s"
                cursor.execute(sql, (tarea))
                resultado = cursor.fetchone()

                if resultado:
                    beneficio_total += resultado[0]

            return beneficio_total
        except Exception as ex:
            print(f"Error al calcular el coste total: {ex}")
            return None


    @staticmethod
    def skills_matching(fabrica_id):
        acciones = TareaModel.obtener_habilidades_subtareas(fabrica_id)
        recursos = RecursosModel.obtener_habilidades_recursos(fabrica_id)
        matching_skills = {}
        for accion_id, habilidades_accion in acciones.items():
            h_tecnicas_accion, h_interpersonales_accion = habilidades_accion

            humanos_validos = []
            for humano_id, habilidades_humano in recursos.items():
                h_tecnicas_humano, h_interpersonales_humano = habilidades_humano

                if (set(h_tecnicas_accion).issubset(set(h_tecnicas_humano)) and
                    set(h_interpersonales_accion).issubset(set(h_interpersonales_humano))):
                    humanos_validos.append(humano_id)

            matching_skills[accion_id] = humanos_validos

        return matching_skills