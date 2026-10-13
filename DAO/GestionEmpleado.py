
from DAO.Conexion import conectar
from DTO.Empleado import Empleado


def insertar(empleado):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        # Normalizar el RUN para evitar diferencias por espacios.
        run = str(empleado.run).strip().upper()

        if not run:
            print("Error: el RUN no puede estar vacío.")
            return

        # Validar que el RUN no esté registrado.
        cursor.execute(
            "SELECT user_id FROM empleado WHERE run = %s",
            (run,)
        )

        if cursor.fetchone():
            print("Error: ya existe un empleado con ese RUN.")
            return

        # Comprobar que el departamento exista.
        cursor.execute(
            "SELECT user_id FROM departamento WHERE user_id = %s",
            (empleado.departamento_id,)
        )

        if not cursor.fetchone():
            print("Error: el departamento seleccionado no existe.")
            return

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
            run,
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

        print(
            "Empleado registrado correctamente. "
            f"ID: {empleado.user_id}"
        )

    except Exception as e:
        conexion.rollback()
        print("Error al registrar empleado:", e)

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
        return cursor.fetchall()

    except Exception as e:
        print("Error al consultar empleados:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(empleado):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        run = str(empleado.run).strip().upper()

        if not run:
            print("Error: el RUN no puede estar vacío.")
            return

        # Comprobar que el empleado exista.
        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (empleado.user_id,)
        )

        if not cursor.fetchone():
            print("Error: el empleado que intentas modificar no existe.")
            return

        # Comprobar que el RUN no pertenezca a otro empleado.
        cursor.execute(
            """
            SELECT user_id
            FROM empleado
            WHERE run = %s
              AND user_id != %s
            """,
            (run, empleado.user_id)
        )

        if cursor.fetchone():
            print("Error: ese RUN ya pertenece a otro empleado.")
            return

        # Comprobar que el departamento exista.
        cursor.execute(
            "SELECT user_id FROM departamento WHERE user_id = %s",
            (empleado.departamento_id,)
        )

        if not cursor.fetchone():
            print("Error: el departamento seleccionado no existe.")
            return

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
            run,
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
            print("No se detectaron cambios en el empleado.")

    except Exception as e:
        conexion.rollback()
        print("Error al modificar empleado:", e)

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

        # Verificar que el empleado exista.
        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (user_id,)
        )

        if not cursor.fetchone():
            print("No existe un empleado con ese ID.")
            return

        # Comprobar asignaciones asociadas.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM asignacion_emp
            WHERE empleado_id = %s
            """,
            (user_id,)
        )
        asignaciones = cursor.fetchone()[0]

        # Comprobar registros de tiempo asociados.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM registro_tiempo
            WHERE empleado_id = %s
            """,
            (user_id,)
        )
        registros_tiempo = cursor.fetchone()[0]

        if asignaciones > 0 or registros_tiempo > 0:
            print(
                "\nNo se puede eliminar el empleado porque tiene "
                "asignaciones o registros de tiempo asociados."
            )
            print(
                "Gestiona primero esos registros para evitar "
                "perder información."
            )
            return

        cursor.execute(
            "DELETE FROM empleado WHERE user_id = %s",
            (user_id,)
        )

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
