
from DAO.Conexion import conectar


def insertar(departamento):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

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

        print(
            f"Departamento registrado correctamente. "
            f"ID: {departamento.user_id}"
        )

    except Exception as e:
        conexion.rollback()
        print("Error al registrar departamento:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()


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
                user_id,
                nombre,
                gerente_empleado_id,
                descripcion
            FROM departamento
            ORDER BY user_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception as e:
        print("Error al consultar departamentos:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(departamento):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

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

        if cursor.rowcount > 0:
            conexion.commit()
            print("Departamento modificado correctamente.")
        else:
            conexion.rollback()
            print(
                "No se encontró el departamento "
                "o no se realizaron cambios."
            )

    except Exception as e:
        conexion.rollback()
        print("Error al modificar departamento:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            DELETE FROM departamento
            WHERE user_id = %s
        """

        cursor.execute(sql, (user_id,))

        if cursor.rowcount > 0:
            conexion.commit()
            print("Departamento eliminado correctamente.")
        else:
            conexion.rollback()
            print("No existe un departamento con ese ID.")

    except Exception as e:
        conexion.rollback()
        print("Error al eliminar departamento:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()
