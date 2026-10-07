from DAO.Conexion import conectar
from DTO.Proyecto import Proyecto


def insertar(proyecto):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO proyecto
                (nombre, descripcion, fecha_inicio)
                VALUES (%s, %s, %s)
            """

            datos = (
                proyecto.nombre,
                proyecto.descripcion,
                proyecto.fecha_inicio
            )

            cursor.execute(sql, datos)

            proyecto.user_id = cursor.lastrowid

            conexion.commit()

            print("Proyecto registrado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar proyecto:", e)

        finally:
            cursor.close()
            conexion.close()


def consultar():
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                SELECT
                    user_id,
                    nombre,
                    descripcion,
                    fecha_inicio
                FROM proyecto
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

            return resultados

        except Exception as e:
            print("Error al consultar proyectos:", e)

        finally:
            cursor.close()
            conexion.close()


def modificar(proyecto):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE proyecto
                SET nombre = %s,
                    descripcion = %s,
                    fecha_inicio = %s
                WHERE user_id = %s
            """

            datos = (
                proyecto.nombre,
                proyecto.descripcion,
                proyecto.fecha_inicio,
                proyecto.user_id
            )

            cursor.execute(sql, datos)

            conexion.commit()

            print("Proyecto modificado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar proyecto:", e)

        finally:
            cursor.close()
            conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM proyecto
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            conexion.commit()

            print("Proyecto eliminado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar proyecto:", e)

        finally:
            cursor.close()
            conexion.close()