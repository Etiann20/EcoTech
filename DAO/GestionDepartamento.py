from DAO.Conexion import conectar
from DTO.Departamento import Departamento


def insertar(departamento):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO departamento
                (nombre, gerente_empleado_id, descripcion)
                VALUES (%s, %s, %s)
            """

            datos = (
                departamento.nombre,
                departamento.gerente_empleado_id,
                departamento.descripcion
            )

            cursor.execute(sql, datos)

            departamento.user_id = cursor.lastrowid

            conexion.commit()

            print("Departamento registrado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar departamento:", e)

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
                    gerente_empleado_id,
                    descripcion
                FROM departamento
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

            return resultados

        except Exception as e:
            print("Error al consultar departamentos:", e)

        finally:
            cursor.close()
            conexion.close()


def modificar(departamento):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE departamento
                SET nombre = %s,
                    gerente_empleado_id = %s,
                    descripcion = %s
                WHERE user_id = %s
            """

            datos = (
                departamento.nombre,
                departamento.gerente_empleado_id,
                departamento.descripcion,
                departamento.user_id
            )

            cursor.execute(sql, datos)

            conexion.commit()

            print("Departamento modificado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar departamento:", e)

        finally:
            cursor.close()
            conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM departamento
                WHERE user_id = %s
            """

            cursor.execute(sql, (user_id,))

            conexion.commit()

            print("Departamento eliminado correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar departamento:", e)

        finally:
            cursor.close()
            conexion.close()