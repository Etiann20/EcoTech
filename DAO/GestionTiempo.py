from DAO.Conexion import conectar
from DTO.RegistroTiempo import RegistroTiempo


def insertar(registro):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """

            datos = (
                registro.empleado_id,
                registro.proyecto_id,
                registro.fecha,
                registro.horas,
                registro.descripcion
            )

            cursor.execute(sql, datos)

            registro.user_id = cursor.lastrowid

            conexion.commit()

            print("Registro de tiempo creado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar tiempo:", e)

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
                    empleado_id,
                    proyecto_id,
                    fecha,
                    horas,
                    descripcion
                FROM registro_tiempo
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

            return resultados

        except Exception as e:
            print("Error al consultar registros de tiempo:", e)

        finally:
            cursor.close()
            conexion.close()


def modificar(registro):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE registro_tiempo
                SET empleado_id = %s,
                    proyecto_id = %s,
                    fecha = %s,
                    horas = %s,
                    descripcion = %s
                WHERE user_id = %s
            """

            datos = (
                registro.empleado_id,
                registro.proyecto_id,
                registro.fecha,
                registro.horas,
                registro.descripcion,
                registro.user_id
            )

            cursor.execute(sql, datos)

            conexion.commit()

            print("Registro de tiempo modificado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar registro de tiempo:", e)

        finally:
            cursor.close()
            conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM registro_tiempo
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            conexion.commit()

            print("Registro de tiempo eliminado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar registro de tiempo:", e)

        finally:
            cursor.close()
            conexion.close()