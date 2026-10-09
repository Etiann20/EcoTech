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

    except Exception as e:
        conexion.rollback()
        print("Error al registrar proyecto:", e)

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

        resultados = cursor.fetchall()

        return resultados

    except Exception as e:
        print("Error al consultar proyectos:", e)
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

    except Exception as e:
        conexion.rollback()
        print("Error al modificar proyecto:", e)

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
        print("Error al eliminar proyecto:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()