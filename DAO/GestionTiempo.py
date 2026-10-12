from DAO.Conexion import conectar
from DTO.RegistroTiempo import RegistroTiempo


# ==================================================
# REGISTRAR TIEMPO
# ==================================================

def insertar(registro):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        # Verificar que el empleado esté asignado al proyecto
        sql_validacion = """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s
              AND proyecto_id = %s
        """

        cursor.execute(
            sql_validacion,
            (registro.empleado_id, registro.proyecto_id)
        )

        if cursor.fetchone() is None:
            print(
                "Error: el empleado no está asignado a este proyecto."
            )
            conexion.rollback()
            return False

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
        return True

    except Exception as e:
        conexion.rollback()
        print("Error al registrar tiempo:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()


# ==================================================
# CONSULTAR REGISTROS DE TIEMPO
# ==================================================

def consultar():
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return []

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                rt.user_id,
                rt.empleado_id,
                e.nombre,
                rt.proyecto_id,
                p.nombre,
                rt.fecha,
                rt.horas,
                rt.descripcion
            FROM registro_tiempo rt
            INNER JOIN empleado e
                ON rt.empleado_id = e.user_id
            INNER JOIN proyecto p
                ON rt.proyecto_id = p.user_id
            ORDER BY rt.user_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception as e:
        print("Error al consultar registros de tiempo:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


# ==================================================
# MODIFICAR REGISTRO DE TIEMPO
# ==================================================

def modificar(registro):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        # Comprobar que la asignación exista
        sql_validacion = """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s
              AND proyecto_id = %s
        """

        cursor.execute(
            sql_validacion,
            (registro.empleado_id, registro.proyecto_id)
        )

        if cursor.fetchone() is None:
            print(
                "Error: el empleado no está asignado a este proyecto."
            )
            conexion.rollback()
            return False

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

        if cursor.rowcount > 0:
            conexion.commit()
            print("Registro de tiempo modificado correctamente.")
            return True

        conexion.rollback()
        print(
            "No se encontró el registro o no se realizaron cambios."
        )
        return False

    except Exception as e:
        conexion.rollback()
        print("Error al modificar registro de tiempo:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()


# ==================================================
# ELIMINAR REGISTRO DE TIEMPO
# ==================================================

def eliminar(user_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            DELETE FROM registro_tiempo
            WHERE user_id = %s
        """

        cursor.execute(sql, (user_id,))

        if cursor.rowcount > 0:
            conexion.commit()
            print("Registro de tiempo eliminado correctamente.")
            return True

        conexion.rollback()
        print("No existe un registro de tiempo con ese ID.")
        return False

    except Exception as e:
        conexion.rollback()
        print("Error al eliminar registro de tiempo:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()