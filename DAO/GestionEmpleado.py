from DAO.Conexion import conectar
from DTO.Empleado import Empleado


def insertar(empleado):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql_persona = """
                INSERT INTO persona
                (run, nombre, direccion, telefono, correo)
                VALUES (%s, %s, %s, %s, %s)
            """

            datos_persona = (
                empleado.run,
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo
            )

            cursor.execute(sql_persona, datos_persona)

            user_id = cursor.lastrowid

            sql_empleado = """
                INSERT INTO empleado
                (user_id, fecha_inicio, salario, departamento_id)
                VALUES (%s, %s, %s, %s)
            """

            datos_empleado = (
                user_id,
                empleado.fecha_inicio,
                empleado.salario,
                empleado.departamento_id
            )

            cursor.execute(sql_empleado, datos_empleado)

            conexion.commit()

            empleado.user_id = user_id

            print("Empleado registrado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar empleado:", e)

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
                    p.user_id,
                    p.run,
                    p.nombre,
                    p.direccion,
                    p.telefono,
                    p.correo,
                    e.fecha_inicio,
                    e.salario,
                    e.departamento_id
                FROM persona p
                INNER JOIN empleado e
                    ON p.user_id = e.user_id
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

            return resultados

        except Exception as e:
            print("Error al consultar empleados:", e)

        finally:
            cursor.close()
            conexion.close()


def modificar(empleado):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql_persona = """
                UPDATE persona
                SET run = %s,
                    nombre = %s,
                    direccion = %s,
                    telefono = %s,
                    correo = %s
                WHERE user_id = %s
            """

            datos_persona = (
                empleado.run,
                empleado.nombre,
                empleado.direccion,
                empleado.telefono,
                empleado.correo,
                empleado.user_id
            )

            cursor.execute(sql_persona, datos_persona)

            sql_empleado = """
                UPDATE empleado
                SET fecha_inicio = %s,
                    salario = %s,
                    departamento_id = %s
                WHERE user_id = %s
            """

            datos_empleado = (
                empleado.fecha_inicio,
                empleado.salario,
                empleado.departamento_id,
                empleado.user_id
            )

            cursor.execute(sql_empleado, datos_empleado)

            conexion.commit()

            print("Empleado modificado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar empleado:", e)

        finally:
            cursor.close()
            conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM persona
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            conexion.commit()

            print("Empleado eliminado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar empleado:", e)

        finally:
            cursor.close()
            conexion.close()