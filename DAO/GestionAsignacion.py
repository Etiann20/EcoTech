from DAO.Conexion import conectar
from DTO.AsignacionEmp import AsignacionEmp


def insertar(asignacion):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                INSERT INTO asignacion_emp
                (empleado_id, proyecto_id, rol)
                VALUES (%s, %s, %s)
            """

            datos = (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.rol
            )

            cursor.execute(sql, datos)

            asignacion.asignacion_id = cursor.lastrowid

            conexion.commit()

            print("Asignación registrada correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al registrar asignación:", e)

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
                    asignacion_id,
                    empleado_id,
                    proyecto_id,
                    rol
                FROM asignacion_emp
            """

            cursor.execute(sql)

            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

            return resultados

        except Exception as e:
            print("Error al consultar asignaciones:", e)

        finally:
            cursor.close()
            conexion.close()


def modificar(asignacion):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                UPDATE asignacion_emp
                SET empleado_id = %s,
                    proyecto_id = %s,
                    rol = %s
                WHERE asignacion_id = %s
            """

            datos = (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.rol,
                asignacion.asignacion_id
            )

            cursor.execute(sql, datos)

            conexion.commit()

            print("Asignación modificada correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al modificar asignación:", e)

        finally:
            cursor.close()
            conexion.close()


def eliminar(asignacion_id):
    conexion = conectar()

    if conexion:
        try:
            cursor = conexion.cursor()

            sql = """
                DELETE FROM asignacion_emp
                WHERE asignacion_id = %s
            """

            cursor.execute(sql, (asignacion_id,))

            conexion.commit()

            print("Asignación eliminada correctamente.")

        except Exception as e:
            conexion.rollback()
            print("Error al eliminar asignación:", e)

        finally:
            cursor.close()
            conexion.close()