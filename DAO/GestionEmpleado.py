from DAO.Conexion import conectar
from DTO.Empleado import Empleado


def insertar(empleado):
    conexion = conectar()

    if conexion:
        cursor = None

        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO empleado
                (
                    run,
                    nombre,
                    direccion,
                    telefono,
                    correo,
                    fecha_inicio,
                    salario,
                    departamento_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            datos = (
                empleado.run,
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo,
                empleado.fecha_inicio,
                empleado.salario,
                empleado.departamento_id
            )

            cursor.execute(sql, datos)

            empleado.user_id = cursor.lastrowid

            conexion.commit()

            print("Empleado registrado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar empleado:", e)

        finally:
            if cursor:
                cursor.close()
            conexion.close()


def consultar():
    conexion = conectar()

    if conexion:
        cursor = None

        try:
            cursor = conexion.cursor()

            sql = """
                SELECT
                    user_id,
                    run,
                    nombre,
                    direccion,
                    telefono,
                    correo,
                    fecha_inicio,
                    salario,
                    departamento_id
                FROM empleado
                ORDER BY user_id
            """

            cursor.execute(sql)
            resultados = cursor.fetchall()

            return resultados

        except Exception as e:
            print("Error al consultar empleados:", e)
            return []

        finally:
            if cursor:
                cursor.close()
            conexion.close()


def modificar(empleado):
    conexion = conectar()

    if conexion:
        cursor = None

        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE empleado
                SET
                    run = %s,
                    nombre = %s,
                    direccion = %s,
                    telefono = %s,
                    correo = %s,
                    fecha_inicio = %s,
                    salario = %s,
                    departamento_id = %s
                WHERE user_id = %s
            """

            datos = (
                empleado.run,
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo,
                empleado.fecha_inicio,
                empleado.salario,
                empleado.departamento_id,
                empleado.user_id
            )

            cursor.execute(sql, datos)

            if cursor.rowcount > 0:
                conexion.commit()
                print("Empleado modificado correctamente.")
            else:
                conexion.rollback()
                print("No se encontró el empleado o no hubo cambios.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar empleado:", e)

        finally:
            if cursor:
                cursor.close()
            conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if conexion:
        cursor = None

        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM empleado
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            if cursor.rowcount > 0:
                conexion.commit()
                print("Empleado eliminado correctamente.")
            else:
                conexion.rollback()
                print("No existe un empleado con ese ID.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar empleado:", e)

        finally:
            if cursor:
                cursor.close()
            conexion.close()