from DAO.Conexion import conectar


def insertar(asignacion):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        # Comprobar que el empleado exista.
        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (asignacion.empleado_id,)
        )

        if not cursor.fetchone():
            print("Error: el empleado seleccionado no existe.")
            return

        # Comprobar que el proyecto exista.
        cursor.execute(
            "SELECT user_id FROM proyecto WHERE user_id = %s",
            (asignacion.proyecto_id,)
        )

        if not cursor.fetchone():
            print("Error: el proyecto seleccionado no existe.")
            return

        # Evitar asignar dos veces al mismo empleado
        # al mismo proyecto.
        sql_duplicado = """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s
              AND proyecto_id = %s
        """

        cursor.execute(
            sql_duplicado,
            (
                asignacion.empleado_id,
                asignacion.proyecto_id
            )
        )

        if cursor.fetchone():
            print(
                "Error: el empleado ya está asignado "
                "a ese proyecto."
            )
            return

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

        print(
            "Asignación registrada correctamente. "
            f"ID: {asignacion.asignacion_id}"
        )

    except Exception as e:
        conexion.rollback()
        print("Error al registrar asignación:", e)

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
                a.asignacion_id,
                a.empleado_id,
                e.nombre,
                a.proyecto_id,
                p.nombre,
                a.rol
            FROM asignacion_emp AS a
            LEFT JOIN empleado AS e
                ON a.empleado_id = e.user_id
            LEFT JOIN proyecto AS p
                ON a.proyecto_id = p.user_id
            ORDER BY a.asignacion_id
        """

        cursor.execute(sql)

        return cursor.fetchall()

    except Exception as e:
        print("Error al consultar asignaciones:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(asignacion):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        # Comprobar que la asignación exista.
        cursor.execute(
            """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE asignacion_id = %s
            """,
            (asignacion.asignacion_id,)
        )

        if not cursor.fetchone():
            print("Error: la asignación no existe.")
            return

        # Comprobar que el empleado exista.
        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (asignacion.empleado_id,)
        )

        if not cursor.fetchone():
            print("Error: el empleado seleccionado no existe.")
            return

        # Comprobar que el proyecto exista.
        cursor.execute(
            "SELECT user_id FROM proyecto WHERE user_id = %s",
            (asignacion.proyecto_id,)
        )

        if not cursor.fetchone():
            print("Error: el proyecto seleccionado no existe.")
            return

        # Evitar duplicados, excluyendo la asignación actual.
        sql_duplicado = """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s
              AND proyecto_id = %s
              AND asignacion_id != %s
        """

        cursor.execute(
            sql_duplicado,
            (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.asignacion_id
            )
        )

        if cursor.fetchone():
            print(
                "Error: el empleado ya está asignado "
                "a ese proyecto."
            )
            return

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

        if cursor.rowcount > 0:
            conexion.commit()
            print("Asignación modificada correctamente.")
        else:
            conexion.rollback()
            print(
                "La asignación existe, pero no se "
                "detectaron cambios."
            )

    except Exception as e:
        conexion.rollback()
        print("Error al modificar asignación:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def eliminar(asignacion_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            DELETE FROM asignacion_emp
            WHERE asignacion_id = %s
        """

        cursor.execute(sql, (asignacion_id,))

        if cursor.rowcount > 0:
            conexion.commit()
            print("Asignación eliminada correctamente.")
        else:
            conexion.rollback()
            print("No existe una asignación con ese ID.")

    except Exception as e:
        conexion.rollback()
        print("Error al eliminar asignación:", e)

    finally:
        if cursor:
            cursor.close()
        conexion.close()