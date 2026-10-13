
from DAO.Conexion import conectar
import pymysql


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

    except pymysql.MySQLError:
        conexion.rollback()
        print("No fue posible registrar el departamento. Verifica los datos e inténtalo nuevamente.")

    except Exception:
        conexion.rollback()
        print("Ocurrió un error inesperado al registrar el departamento.")

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

    except Exception:
        print("No fue posible consultar los departamentos.")
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

    except pymysql.MySQLError:
        conexion.rollback()
        print("No fue posible modificar el departamento. Verifica los datos e inténtalo nuevamente.")

    except Exception:
        conexion.rollback()
        print("Ocurrió un error inesperado al modificar el departamento.")

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

    except pymysql.MySQLError as e:
        conexion.rollback()

        if e.args and e.args[0] == 1451:
            print(
                "\nNo se puede eliminar el departamento porque "
                "tiene empleados asociados."
            )
        else:
            print("No fue posible eliminar el departamento.")

    except Exception:
        conexion.rollback()
        print("Ocurrió un error inesperado al eliminar el departamento.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()
