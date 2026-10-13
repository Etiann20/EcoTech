
from DAO.Conexion import conectar


def insertar(proyecto):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

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

        print(
            f"Proyecto registrado correctamente. "
            f"ID: {proyecto.user_id}"
        )

    except Exception:
        conexion.rollback()
        print("No fue posible registrar el proyecto.")

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
                descripcion,
                fecha_inicio
            FROM proyecto
            ORDER BY user_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("No fue posible consultar los proyectos.")
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(proyecto):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

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

        if cursor.rowcount > 0:
            conexion.commit()
            print("Proyecto modificado correctamente.")
        else:
            conexion.rollback()
            print(
                "No se encontró el proyecto "
                "o no se realizaron cambios."
            )

    except Exception:
        conexion.rollback()
        print("No fue posible modificar el proyecto.")

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
            DELETE FROM proyecto
            WHERE user_id = %s
        """

        cursor.execute(sql, (user_id,))

        if cursor.rowcount > 0:
            conexion.commit()
            print("Proyecto eliminado correctamente.")
        else:
            conexion.rollback()
            print("No existe un proyecto con ese ID.") 

    except Exception as e:
        conexion.rollback()

        if e.args and e.args[0] == 1451:
            print(
                "No se puede eliminar el proyecto porque "
                "tiene asignaciones o registros asociados."
            )
        else:
            print("No fue posible eliminar el proyecto.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def consultar_empleados():
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return []

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT user_id, nombre
            FROM empleado
            ORDER BY user_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("No fue posible consultar los empleados.")
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def consultar_por_empleado(empleado_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return []

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                p.user_id,
                p.nombre,
                p.descripcion,
                p.fecha_inicio,
                a.rol
            FROM asignacion_emp AS a
            INNER JOIN proyecto AS p
                ON a.proyecto_id = p.user_id
            WHERE a.empleado_id = %s
            ORDER BY p.user_id
        """

        cursor.execute(sql, (empleado_id,))
        return cursor.fetchall()

    except Exception:
        print(
            "No fue posible consultar los proyectos del empleado."
        )
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()
