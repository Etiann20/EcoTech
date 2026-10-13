from datetime import datetime

from DTO.Departamento import Departamento
from DTO.Empleado import Empleado
from DTO.Proyecto import Proyecto
from DTO.AsignacionEmp import AsignacionEmp
from DTO.RegistroTiempo import RegistroTiempo

from DAO import GestionDepartamento
from DAO import GestionEmpleado
from DAO import GestionProyecto
from DAO import GestionAsignacion
from DAO import GestionTiempo


# ==================================================
# NAVEGACIÓN Y VALIDACIÓN DE DATOS
# ==================================================

def validar_run_disponible(valor):
    run = str(valor).strip().upper()

    conexion = None
    cursor = None

    try:
        from DAO.Conexion import conectar

        conexion = conectar()

        if not conexion:
            return "No fue posible conectar con la base de datos."

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM empleado WHERE run = %s",
            (run,)
        )

        if cursor.fetchone():
            return "Ya existe un empleado con ese RUN."

        return None

    except Exception as e:
        return f"No se pudo validar el RUN: {e}"

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()

def validar_run_modificacion(valor, user_id):
    run = str(valor).strip().upper()

    conexion = None
    cursor = None

    try:
        from DAO.Conexion import conectar

        conexion = conectar()

        if not conexion:
            return "No fue posible conectar con la base de datos."

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT user_id
            FROM empleado
            WHERE run = %s
              AND user_id <> %s
            """,
            (run, user_id)
        )

        if cursor.fetchone():
            return "Ya existe otro empleado con ese RUN."

        return None

    except Exception as e:
        return f"No se pudo validar el RUN: {e}"

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def leer_formulario(campos):
    """
    Lee los campos de un formulario y permite:
    <<         Volver al campo anterior.
    CANCELAR   Cancelar la operación actual.
    SALIR      Volver al menú del módulo.
    """
    datos = {}
    indice = 0

    print("\nComandos disponibles:")
    print("  <<         Volver al campo anterior")
    print("  CANCELAR   Cancelar esta operación")
    print("  SALIR      Volver al menú del módulo")
    print("-" * 55)

    while indice < len(campos):
        nombre, mensaje, tipo, validador = campos[indice]
        entrada = input(mensaje).strip()

        if entrada == "<<":
            if indice == 0:
                print("Ya estás en el primer campo.")
            else:
                indice -= 1
                campo = campos[indice][0]
                print(
                    f"Volviendo al campo '{campo}'. "
                    f"Valor anterior: {datos.get(campo, '')}"
                )
            continue

        if entrada.upper() == "CANCELAR":
            print("Operación cancelada. No se guardaron cambios.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú del módulo.")
            return "SALIR"

        try:
            if tipo == "texto":
                if not entrada:
                    raise ValueError("El campo no puede estar vacío.")
                valor = entrada

            elif tipo == "entero":
                valor = int(entrada)

            elif tipo == "fecha":
                valor = datetime.strptime(
                    entrada, "%Y-%m-%d"
                ).date()

            else:
                valor = entrada

            if validador is not None:
                error = validador(valor)
                if error:
                    raise ValueError(error)

            datos[nombre] = valor
            indice += 1

        except ValueError as error:
            print("Error:", error)

    return datos


def validar_positivo(valor):
    if valor <= 0:
        return "El valor debe ser mayor que cero."
    return None


def validar_no_negativo(valor):
    if valor < 0:
        return "El valor no puede ser negativo."
    return None


def validar_correo(valor):
    valor = str(valor).strip()

    if (
        not valor
        or " " in valor
        or "@" not in valor
        or valor.startswith("@")
        or valor.endswith("@")
        or "." not in valor.split("@")[-1]
    ):
        return "Ingresa un correo válido, por ejemplo usuario@correo.cl."

    return None


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto.upper() in ("CANCELAR", "SALIR"):
            return None

        if texto == "<<":
            print(
                "Para retroceder entre campos, utiliza "
                "este comando dentro de un formulario."
            )
            continue

        if not texto:
            print("Error: el campo no puede estar vacío.")
            continue

        return texto


def leer_entero(mensaje):
    while True:
        entrada = input(mensaje).strip()

        if entrada.upper() == "CANCELAR":
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            return "SALIR"

        if entrada == "<<":
            print(
                "Para retroceder entre campos, utiliza "
                "este comando dentro de un formulario."
            )
            continue

        try:
            return int(entrada)
        except ValueError:
            print("Error: debes ingresar un número entero.")


def leer_fecha(mensaje):
    while True:
        entrada = input(mensaje).strip()

        if entrada.upper() in ("CANCELAR", "SALIR"):
            return None

        if entrada == "<<":
            print(
                "Para retroceder entre campos, utiliza "
                "este comando dentro de un formulario."
            )
            continue

        try:
            return datetime.strptime(
                entrada, "%Y-%m-%d"
            ).date()
        except ValueError:
            print(
                "Error: usa una fecha válida "
                "con formato YYYY-MM-DD."
            )



# ==================================================
# CONFIRMACIONES
# ==================================================



# ==================================================
# CONFIRMACIONES
# ==================================================

def confirmar_operacion(mensaje):
    while True:
        respuesta = input(
            f"{mensaje}\n"
            "Escribe SÍ, NO, CANCELAR o SALIR: "
        ).strip().lower()

        if respuesta in ("si", "sí", "s"):
            return True

        elif respuesta in ("no", "n", "cancelar"):
            print("Operación cancelada. No se guardaron cambios.")
            return False

        elif respuesta == "salir":
            print("Volviendo al menú del módulo.")
            return "SALIR"

        elif respuesta == "<<":
            print("No hay un campo anterior en la confirmación.")

        else:
            print("Respuesta no válida.")


def confirmar_eliminacion():
    return confirmar_operacion(
        "¿Está realmente seguro que quiere eliminar?"
    )


def confirmar_asignacion(accion="registrar"):
    return confirmar_operacion(
        f"¿Confirma que desea {accion} esta asignación?"
    )

# ==================================================
# MOSTRAR DEPARTAMENTOS
# ==================================================

def mostrar_departamentos():
    departamentos = GestionDepartamento.consultar()

    if not departamentos:
        print("No hay departamentos registrados.")
        return []

    print("\n" + "=" * 85)
    print(
        f"{'ID':<8}"
        f"{'Nombre':<25}"
        f"{'Gerente ID':<15}"
        f"Descripción"
    )
    print("-" * 85)

    for fila in departamentos:
        user_id, nombre, gerente_id, descripcion = fila

        gerente = (
            str(gerente_id)
            if gerente_id is not None
            else "Sin asignar"
        )

        descripcion = (
            descripcion
            if descripcion is not None
            else "Sin descripción"
        )

        print(
            f"{user_id:<8}"
            f"{nombre:<25}"
            f"{gerente:<15}"
            f"{descripcion}"
        )

    print("=" * 85)
    return departamentos


# ==================================================
# MOSTRAR EMPLEADOS
# ==================================================

def mostrar_empleados():
    empleados = GestionEmpleado.consultar()

    if not empleados:
        print("No hay empleados registrados.")
        return []

    print("\n" + "=" * 145)
    print(
        f"{'ID':<6}"
        f"{'RUN':<16}"
        f"{'Nombre':<22}"
        f"{'Dirección':<25}"
        f"{'Teléfono':<13}"
        f"{'Correo':<27}"
        f"{'Fecha inicio':<15}"
        f"{'Salario':<12}"
        f"Departamento"
    )
    print("-" * 145)

    for fila in empleados:
        (
            user_id,
            run,
            nombre,
            direccion,
            telefono,
            correo,
            fecha_inicio,
            salario,
            departamento_id
        ) = fila

        departamento = (
            str(departamento_id)
            if departamento_id is not None
            else "Sin asignar"
        )

        print(
            f"{user_id:<6}"
            f"{str(run):<16}"
            f"{str(nombre):<22}"
            f"{str(direccion):<25}"
            f"{str(telefono):<13}"
            f"{str(correo):<27}"
            f"{str(fecha_inicio):<15}"
            f"{str(salario):<12}"
            f"{departamento}"
        )

    print("=" * 145)
    return empleados


# ==================================================
# MOSTRAR PROYECTOS
# ==================================================

def mostrar_proyectos():
    proyectos = GestionProyecto.consultar()

    if not proyectos:
        print("No hay proyectos registrados.")
        return []

    print("\n" + "=" * 100)
    print(
        f"{'ID':<8}"
        f"{'Nombre':<30}"
        f"{'Fecha inicio':<18}"
        f"Descripción"
    )
    print("-" * 100)

    for fila in proyectos:
        user_id, nombre, descripcion, fecha_inicio = fila

        descripcion = (
            descripcion
            if descripcion is not None
            else "Sin descripción"
        )

        fecha_inicio = (
            fecha_inicio
            if fecha_inicio is not None
            else "Sin definir"
        )

        print(
            f"{user_id:<8}"
            f"{nombre:<30}"
            f"{str(fecha_inicio):<18}"
            f"{descripcion}"
        )

    print("=" * 100)
    return proyectos


# ==================================================
# MOSTRAR ASIGNACIONES
# ==================================================

def mostrar_asignaciones():
    asignaciones = GestionAsignacion.consultar()

    if not asignaciones:
        print("No hay asignaciones registradas.")
        return []

    print("\n" + "=" * 115)
    print(
        f"{'ID':<8}"
        f"{'ID Empleado':<14}"
        f"{'Empleado':<25}"
        f"{'ID Proyecto':<14}"
        f"{'Proyecto':<25}"
        f"Rol"
    )
    print("-" * 115)

    for fila in asignaciones:
        (
            asignacion_id,
            empleado_id,
            empleado_nombre,
            proyecto_id,
            proyecto_nombre,
            rol
        ) = fila

        empleado_nombre = (
            empleado_nombre
            if empleado_nombre is not None
            else "Sin asignar"
        )

        proyecto_nombre = (
            proyecto_nombre
            if proyecto_nombre is not None
            else "Sin asignar"
        )

        rol = rol if rol is not None else "Sin definir"

        print(
            f"{asignacion_id:<8}"
            f"{empleado_id:<14}"
            f"{empleado_nombre:<25}"
            f"{proyecto_id:<14}"
            f"{proyecto_nombre:<25}"
            f"{rol}"
        )

    print("=" * 115)
    return asignaciones


# ==================================================
# SELECCIONAR DEPARTAMENTO
# ==================================================


def seleccionar_departamento():
    departamentos = mostrar_departamentos()

    if not departamentos:
        print(
            "No se puede continuar. "
            "Primero debes registrar un departamento."
        )
        return None

    ids_disponibles = [fila[0] for fila in departamentos]

    while True:
        entrada = input(
            "ID del departamento "
            "(CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            print("Selección cancelada.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú del módulo.")
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del departamento.")
            continue

        try:
            departamento_id = int(entrada)

            if departamento_id in ids_disponibles:
                return departamento_id

            print("Error: selecciona un ID de la tabla.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


# ==================================================
# CRUD DE DEPARTAMENTOS
# ==================================================



def menu_departamentos():
    while True:
        print("\n===== GESTIÓN DE DEPARTAMENTOS =====")
        print("1. Registrar departamento")
        print("2. Consultar departamentos")
        print("3. Modificar departamento")
        print("4. Eliminar departamento")
        print("0. Volver")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion == "SALIR" or opcion == "CANCELAR":
            break

        if opcion is None:
            continue

        if opcion == 0:
            break

        elif opcion == 1:
            print("\n--- Registrar departamento ---")

            datos = leer_formulario([
                ("nombre", "Nombre: ", "texto", None),
                ("descripcion", "Descripción: ", "texto", None),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            departamento = Departamento(
                nombre=datos["nombre"],
                descripcion=datos["descripcion"]
            )

            GestionDepartamento.insertar(departamento)

        elif opcion == 2:
            print("\n--- Departamentos registrados ---")
            mostrar_departamentos()

        elif opcion == 3:
            print("\n--- Modificar departamento ---")

            departamentos = mostrar_departamentos()

            if not departamentos:
                continue

            ids_disponibles = [fila[0] for fila in departamentos]
            user_id = None

            while True:
                entrada = input(
                    "ID del departamento a modificar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print(
                        "Error: selecciona un ID "
                        "que aparezca en la tabla."
                    )

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            datos = leer_formulario([
                ("nombre", "Nuevo nombre: ", "texto", None),
                ("descripcion", "Nueva descripción: ", "texto", None),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            gerente_id = next(
                (
                    fila[2]
                    for fila in departamentos
                    if fila[0] == user_id
                ),
                None
            )

            departamento = Departamento(
                nombre=datos["nombre"],
                descripcion=datos["descripcion"],
                gerente_empleado_id=gerente_id,
                user_id=user_id
            )

            GestionDepartamento.modificar(departamento)

        elif opcion == 4:
            print("\n--- Eliminar departamento ---")

            departamentos = mostrar_departamentos()

            if not departamentos:
                continue

            ids_disponibles = [fila[0] for fila in departamentos]
            user_id = None

            while True:
                entrada = input(
                    "ID del departamento a eliminar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print(
                        "Error: selecciona un ID "
                        "que aparezca en la tabla."
                    )

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            respuesta = confirmar_eliminacion()

            if respuesta == "SALIR":
                break

            if respuesta is True:
                GestionDepartamento.eliminar(user_id)

        else:
            print("Error: opción no válida.")


# ==================================================
# CRUD DE EMPLEADOS
# ==================================================



def menu_empleados():
    while True:
        print("\n========== GESTIÓN DE EMPLEADOS ==========")
        print("1. Registrar empleado")
        print("2. Consultar empleados")
        print("3. Modificar empleado")
        print("4. Eliminar empleado")
        print("0. Volver")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion in ("CANCELAR", "SALIR"):
            break

        if opcion is None:
            continue

        if opcion == 0:
            break

        # ------------------------------------------
        # REGISTRAR EMPLEADO
        # ------------------------------------------
        elif opcion == 1:
            print("\n--- Registrar empleado ---")

            departamento_id = seleccionar_departamento()

            if departamento_id in (None, "CANCELAR"):
                continue

            if departamento_id == "SALIR":
                break

            datos = leer_formulario([
                ("run", "RUN: ", "texto", validar_run_disponible),
                ("nombre", "Nombre: ", "texto", None),
                ("direccion", "Dirección: ", "texto", None),
                (
                    "telefono",
                    "Teléfono (solo números): ",
                    "entero",
                    validar_no_negativo
                ),
                ("correo", "Correo: ", "texto", validar_correo),
                (
                    "fecha_inicio",
                    "Fecha de inicio (YYYY-MM-DD): ",
                    "fecha",
                    None
                ),
                (
                    "salario",
                    "Salario: ",
                    "entero",
                    validar_no_negativo
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            empleado = Empleado(
                run=datos["run"],
                nombre=datos["nombre"],
                direccion=datos["direccion"],
                telefono=datos["telefono"],
                correo=datos["correo"],
                fecha_inicio=datos["fecha_inicio"],
                salario=datos["salario"],
                departamento_id=departamento_id
            )

            GestionEmpleado.insertar(empleado)

        # ------------------------------------------
        # CONSULTAR EMPLEADOS
        # ------------------------------------------
        elif opcion == 2:
            print("\n--- Empleados registrados ---")
            mostrar_empleados()

        # ------------------------------------------
        # MODIFICAR EMPLEADO
        # ------------------------------------------
        elif opcion == 3:
            print("\n--- Modificar empleado ---")

            empleados = mostrar_empleados()

            if not empleados:
                continue

            ids_disponibles = [fila[0] for fila in empleados]
            user_id = None

            while True:
                entrada = input(
                    "ID del empleado que deseas modificar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            departamento_id = seleccionar_departamento()

            if departamento_id in (None, "CANCELAR"):
                continue

            if departamento_id == "SALIR":
                break

            datos = leer_formulario([
                ("run", "Nuevo RUN: ", "texto",
                lambda valor: validar_run_modificacion(valor, user_id)),
                ("nombre", "Nuevo nombre: ", "texto", None),
                ("direccion", "Nueva dirección: ", "texto", None),
                (
                    "telefono",
                    "Nuevo teléfono (solo números): ",
                    "entero",
                    validar_no_negativo
                ),
                ("correo", "Nuevo correo: ", "texto", validar_correo),                
                (
                    "fecha_inicio",
                    "Nueva fecha de inicio (YYYY-MM-DD): ",
                    "fecha",
                    None
                ),
                (
                    "salario",
                    "Nuevo salario: ",
                    "entero",
                    validar_no_negativo
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            empleado = Empleado(
                run=datos["run"],
                nombre=datos["nombre"],
                direccion=datos["direccion"],
                telefono=datos["telefono"],
                correo=datos["correo"],
                fecha_inicio=datos["fecha_inicio"],
                salario=datos["salario"],
                departamento_id=departamento_id,
                user_id=user_id
            )

            GestionEmpleado.modificar(empleado)

        # ------------------------------------------
        # ELIMINAR EMPLEADO
        # ------------------------------------------
        elif opcion == 4:
            print("\n--- Eliminar empleado ---")

            empleados = mostrar_empleados()

            if not empleados:
                continue

            ids_disponibles = [fila[0] for fila in empleados]
            user_id = None

            while True:
                entrada = input(
                    "ID del empleado que deseas eliminar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            respuesta = confirmar_eliminacion()

            if respuesta == "SALIR":
                break

            if respuesta is True:
                GestionEmpleado.eliminar(user_id)

        else:
            print("Error: opción no válida.")




# ==================================================
# CRUD DE PROYECTOS
# ==================================================


def menu_proyectos():
    while True:
        print("\n========== GESTIÓN DE PROYECTOS ==========")
        print("1. Registrar proyecto")
        print("2. Consultar proyectos")
        print("3. Modificar proyecto")
        print("4. Eliminar proyecto")
        print("0. Volver")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion in ("CANCELAR", "SALIR"):
            break

        if opcion is None:
            continue

        if opcion == 0:
            break

        # ------------------------------------------
        # REGISTRAR PROYECTO
        # ------------------------------------------
        elif opcion == 1:
            print("\n--- Registrar proyecto ---")

            datos = leer_formulario([
                ("nombre", "Nombre: ", "texto", None),
                ("descripcion", "Descripción: ", "texto", None),
                (
                    "fecha_inicio",
                    "Fecha de inicio (YYYY-MM-DD): ",
                    "fecha",
                    None
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            proyecto = Proyecto(
                nombre=datos["nombre"],
                descripcion=datos["descripcion"],
                fecha_inicio=datos["fecha_inicio"]
            )

            GestionProyecto.insertar(proyecto)

        
        # ------------------------------------------
        # CONSULTAR PROYECTOS
        # ------------------------------------------
        elif opcion == 2:
            print("\n--- Consultar proyectos ---")
            print("1. Todos los proyectos")
            print("2. Proyectos de un empleado")
            print("0. Volver")

            tipo_consulta = leer_entero(
                "Seleccione una opción: "
            )

            if tipo_consulta == "SALIR":
                break

            if tipo_consulta == "CANCELAR":
                continue

            if tipo_consulta == 0:
                continue

            elif tipo_consulta == 1:
                print("\n--- Todos los proyectos ---")
                mostrar_proyectos()

            elif tipo_consulta == 2:
                print("\n--- Seleccionar empleado ---")

                empleados = GestionProyecto.consultar_empleados()

                if not empleados:
                    print("No hay empleados registrados.")
                    continue

                print("-" * 45)
                print(f"{'ID':<10}{'Nombre':<35}")
                print("-" * 45)

                for empleado in empleados:
                    print(f"{empleado[0]:<10}{empleado[1]:<35}")

                print("-" * 45)

                empleado_id = leer_entero(
                    "ID del empleado (CANCELAR o SALIR): "
                )

                if empleado_id == "SALIR":
                    break

                if empleado_id == "CANCELAR":
                    continue

                if empleado_id is None:
                    continue

                empleado_seleccionado = next(
                    (
                        empleado
                        for empleado in empleados
                        if empleado[0] == empleado_id
                    ),
                    None
                )

                if empleado_seleccionado is None:
                    print("Error: selecciona un ID de empleado válido.")
                    continue

                proyectos = GestionProyecto.consultar_por_empleado(
                    empleado_id
                )

                print(
                    f"\n--- Proyectos de "
                    f"{empleado_seleccionado[1]} ---"
                )

                if not proyectos:
                    print(
                        "Este empleado no tiene proyectos asignados."
                    )
                    continue

                print("-" * 100)
                print(
                    f"{'ID':<6}"
                    f"{'Proyecto':<25}"
                    f"{'Descripción':<35}"
                    f"{'Fecha inicio':<18}"
                    f"{'Rol':<16}"
                )
                print("-" * 100)

                for proyecto in proyectos:
                    fecha = (
                        str(proyecto[3])
                        if proyecto[3] is not None
                        else "Sin fecha"
                    )

                    descripcion = (
                        proyecto[2]
                        if proyecto[2]
                        else "Sin descripción"
                    )

                    rol = (
                        proyecto[4]
                        if proyecto[4]
                        else "Sin rol"
                    )

                    print(
                        f"{proyecto[0]:<6}"
                        f"{proyecto[1][:24]:<25}"
                        f"{descripcion[:34]:<35}"
                        f"{fecha:<18}"
                        f"{rol[:15]:<16}"
                    )

                print("-" * 100)

            else:
                print("Error: opción no válida.")


        # ------------------------------------------
        # MODIFICAR PROYECTO
        # ------------------------------------------
        elif opcion == 3:
            print("\n--- Modificar proyecto ---")

            proyectos = mostrar_proyectos()

            if not proyectos:
                continue

            ids_disponibles = [fila[0] for fila in proyectos]
            user_id = None

            while True:
                entrada = input(
                    "ID del proyecto que deseas modificar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            datos = leer_formulario([
                ("nombre", "Nuevo nombre: ", "texto", None),
                ("descripcion", "Nueva descripción: ", "texto", None),
                (
                    "fecha_inicio",
                    "Nueva fecha de inicio (YYYY-MM-DD): ",
                    "fecha",
                    None
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            proyecto = Proyecto(
                nombre=datos["nombre"],
                descripcion=datos["descripcion"],
                fecha_inicio=datos["fecha_inicio"],
                user_id=user_id
            )

            GestionProyecto.modificar(proyecto)

        # ------------------------------------------
        # ELIMINAR PROYECTO
        # ------------------------------------------
        elif opcion == 4: 
            print("\n--- Eliminar proyecto ---")

            proyectos = mostrar_proyectos()

            if not proyectos:
                continue

            ids_disponibles = [fila[0] for fila in proyectos]
            user_id = None

            while True:
                entrada = input(
                    "ID del proyecto que deseas eliminar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección del ID.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        user_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if user_id is None:
                continue

            respuesta = confirmar_eliminacion()

            if respuesta == "SALIR":
                break

            if respuesta is True:
                GestionProyecto.eliminar(user_id)

        else:
            print("Error: opción no válida.")


# ==================================================
# SELECCIÓN GUIADA PARA ASIGNACIONES
# ==================================================



def seleccionar_empleado_asignacion():
    empleados = GestionEmpleado.consultar()

    if not empleados:
        print("No hay empleados registrados.")
        print("Primero debes registrar un empleado.")
        return None

    print("\n========== EMPLEADOS DISPONIBLES ==========")
    print(f"{'ID EMPLEADO':<15}{'RUN':<20}{'NOMBRE':<30}")
    print("-" * 65)

    for fila in empleados:
        user_id, run, nombre = fila[0], fila[1], fila[2]
        print(f"{user_id:<15}{str(run):<20}{str(nombre):<30}")

    print("=" * 65)

    ids_disponibles = [fila[0] for fila in empleados]

    while True:
        entrada = input(
            "Ingrese el ID del empleado "
            "(CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            print("Selección de empleado cancelada.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú anterior.")
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del empleado.")
            continue

        try:
            empleado_id = int(entrada)

            if empleado_id in ids_disponibles:
                empleado = next(
                    fila for fila in empleados
                    if fila[0] == empleado_id
                )
                return empleado_id, empleado[2]

            print("Error: ese ID no existe.")
            print("Selecciona uno de los IDs de la tabla.")

        except ValueError:
            print("Error: ingresa un número entero.")



def seleccionar_proyecto_asignacion():
    proyectos = GestionProyecto.consultar()

    if not proyectos:
        print("No hay proyectos registrados.")
        print("Primero debes registrar un proyecto.")
        return None

    print("\n========== PROYECTOS DISPONIBLES ==========")
    print(f"{'ID PROYECTO':<15}{'NOMBRE':<30}{'FECHA INICIO':<18}")
    print("-" * 63)

    for fila in proyectos:
        user_id, nombre, descripcion, fecha_inicio = fila

        fecha = (
            str(fecha_inicio)
            if fecha_inicio is not None
            else "Sin definir"
        )

        print(f"{user_id:<15}{str(nombre):<30}{fecha:<18}")

    print("=" * 63)

    ids_disponibles = [fila[0] for fila in proyectos]

    while True:
        entrada = input(
            "Ingrese el ID del proyecto "
            "(CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            print("Selección de proyecto cancelada.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú anterior.")
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del proyecto.")
            continue

        try:
            proyecto_id = int(entrada)

            if proyecto_id in ids_disponibles:
                proyecto = next(
                    fila for fila in proyectos
                    if fila[0] == proyecto_id
                )
                return proyecto_id, proyecto[1]

            print("Error: ese ID no existe.")
            print("Selecciona uno de los IDs de la tabla.")

        except ValueError:
            print("Error: ingresa un número entero.")


# ==================================================
# CRUD DE ASIGNACIONES
# ==================================================


def menu_asignaciones():
    while True:
        print("\n===== ASIGNACIÓN DE EMPLEADOS A PROYECTOS =====")
        print("1. Registrar asignación")
        print("2. Consultar asignaciones")
        print("3. Modificar asignación")
        print("4. Eliminar asignación")
        print("0. Volver")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion in ("CANCELAR", "SALIR"):
            break

        if opcion is None:
            continue

        if opcion == 0:
            break

        # ------------------------------------------
        # REGISTRAR ASIGNACIÓN
        # ------------------------------------------
        elif opcion == 1:
            print("\n--- Registrar asignación ---")

            empleado_seleccionado = seleccionar_empleado_asignacion()

            if empleado_seleccionado is None:
                continue

            if empleado_seleccionado == "CANCELAR":
                continue

            if empleado_seleccionado == "SALIR":
                break

            empleado_id, empleado_nombre = empleado_seleccionado

            proyecto_seleccionado = seleccionar_proyecto_asignacion()

            if proyecto_seleccionado is None:
                continue

            if proyecto_seleccionado == "CANCELAR":
                continue

            if proyecto_seleccionado == "SALIR":
                break

            proyecto_id, proyecto_nombre = proyecto_seleccionado

            datos = leer_formulario([
                ("rol", "Rol del empleado en el proyecto: ", "texto", None),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            rol = datos["rol"]

            print("\n========== RESUMEN DE LA ASIGNACIÓN ==========")
            print(f"ID empleado: {empleado_id}")
            print(f"Empleado:    {empleado_nombre}")
            print(f"ID proyecto: {proyecto_id}")
            print(f"Proyecto:    {proyecto_nombre}")
            print(f"Rol:         {rol}")
            print("=" * 48)

            respuesta = confirmar_asignacion("registrar")

            if respuesta == "SALIR":
                break

            if respuesta is True:
                asignacion = AsignacionEmp(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    rol=rol
                )
                GestionAsignacion.insertar(asignacion)

        # ------------------------------------------
        # CONSULTAR ASIGNACIONES
        # ------------------------------------------
        elif opcion == 2:
            print("\n--- Asignaciones registradas ---")
            mostrar_asignaciones()

        # ------------------------------------------
        # MODIFICAR ASIGNACIÓN
        # ------------------------------------------
        elif opcion == 3:
            print("\n--- Modificar asignación ---")

            asignaciones = mostrar_asignaciones()

            if not asignaciones:
                continue

            ids_disponibles = [fila[0] for fila in asignaciones]
            asignacion_id = None

            while True:
                entrada = input(
                    "ID de la asignación que deseas modificar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección de la asignación.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        asignacion_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if asignacion_id is None:
                continue

            empleado_seleccionado = seleccionar_empleado_asignacion()

            if empleado_seleccionado is None:
                continue

            if empleado_seleccionado == "CANCELAR":
                continue

            if empleado_seleccionado == "SALIR":
                break

            empleado_id, empleado_nombre = empleado_seleccionado

            proyecto_seleccionado = seleccionar_proyecto_asignacion()

            if proyecto_seleccionado is None:
                continue

            if proyecto_seleccionado == "CANCELAR":
                continue

            if proyecto_seleccionado == "SALIR":
                break

            proyecto_id, proyecto_nombre = proyecto_seleccionado

            datos = leer_formulario([
                ("rol", "Nuevo rol: ", "texto", None),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            rol = datos["rol"]

            print("\n========== RESUMEN DE LA MODIFICACIÓN ==========")
            print(f"ID asignación: {asignacion_id}")
            print(f"Empleado: {empleado_nombre} (ID: {empleado_id})")
            print(f"Proyecto: {proyecto_nombre} (ID: {proyecto_id})")
            print(f"Nuevo rol: {rol}")
            print("=" * 50)

            respuesta = confirmar_asignacion("modificar")

            if respuesta == "SALIR":
                break

            if respuesta is True:
                asignacion = AsignacionEmp(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    rol=rol,
                    asignacion_id=asignacion_id
                )
                GestionAsignacion.modificar(asignacion)

        # ------------------------------------------
        # ELIMINAR ASIGNACIÓN
        # ------------------------------------------
        elif opcion == 4:
            print("\n--- Eliminar asignación ---")

            asignaciones = mostrar_asignaciones()

            if not asignaciones:
                continue

            ids_disponibles = [fila[0] for fila in asignaciones]
            asignacion_id = None

            while True:
                entrada = input(
                    "ID de la asignación que deseas eliminar "
                    "(CANCELAR o SALIR para volver): "
                ).strip()

                if entrada.upper() == "CANCELAR":
                    break

                if entrada.upper() == "SALIR":
                    return

                if entrada == "<<":
                    print("Estás en la selección de la asignación.")
                    continue

                try:
                    id_seleccionado = int(entrada)

                    if id_seleccionado in ids_disponibles:
                        asignacion_id = id_seleccionado
                        break

                    print("Error: selecciona un ID de la tabla.")

                except ValueError:
                    print("Error: ingresa un ID numérico.")

            if asignacion_id is None:
                continue

            respuesta = confirmar_eliminacion()

            if respuesta == "SALIR":
                break

            if respuesta is True:
                GestionAsignacion.eliminar(asignacion_id)

        else:
            print("Error: opción no válida.")


# ==================================================
# MOSTRAR REGISTROS DE TIEMPO
# ==================================================

def mostrar_registros_tiempo():
    registros = GestionTiempo.consultar()

    if not registros:
        print("No hay registros de tiempo registrados.")
        return []

    encabezados = [
        "ID", "ID empleado", "Empleado",
        "ID proyecto", "Proyecto", "Fecha",
        "Horas", "Descripción"
    ]

    filas = []

    for registro in registros:
        filas.append([
            str(registro[0]),
            str(registro[1]),
            str(registro[2] or "Sin asignar"),
            str(registro[3]),
            str(registro[4] or "Sin asignar"),
            str(registro[5]),
            str(registro[6]),
            str(registro[7] or "Sin descripción")
        ])

    anchos = [
        max(
            len(encabezados[i]),
            max(len(fila[i]) for fila in filas)
        )
        for i in range(len(encabezados))
    ]

    separador = "+" + "+".join(
        "-" * (ancho + 2) for ancho in anchos
    ) + "+"

    print("\n" + separador)
    print("| " + " | ".join(
        encabezados[i].ljust(anchos[i])
        for i in range(len(encabezados))
    ) + " |")
    print(separador)

    for fila in filas:
        print("| " + " | ".join(
            fila[i].ljust(anchos[i])
            for i in range(len(fila))
        ) + " |")

    print(separador)
    return registros


# ==================================================
# SELECCIONAR EMPLEADO PARA REGISTRO DE TIEMPOS
# ==================================================



def seleccionar_empleado_tiempo():
    empleados = GestionEmpleado.consultar()

    if not empleados:
        print("No hay empleados registrados.")
        print("Primero debes registrar un empleado.")
        return None

    print("\n========== EMPLEADOS DISPONIBLES ==========")
    print(f"{'ID':<10}{'RUN':<20}{'NOMBRE':<30}")
    print("-" * 60)

    for empleado in empleados:
        print(
            f"{str(empleado[0]):<10}"
            f"{str(empleado[1]):<20}"
            f"{str(empleado[2]):<30}"
        )

    print("-" * 60)

    ids_disponibles = [int(empleado[0]) for empleado in empleados]

    while True:
        entrada = input(
            "ID del empleado (CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            print("Selección de empleado cancelada.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú anterior.")
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del empleado.")
            continue

        try:
            empleado_id = int(entrada)

            if empleado_id in ids_disponibles:
                return empleado_id

            print("Error: selecciona un ID de la tabla.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


# ==================================================
# SELECCIONAR PROYECTO ASIGNADO AL EMPLEADO
# ==================================================


def seleccionar_proyecto_tiempo(empleado_id):
    asignaciones = GestionAsignacion.consultar()

    proyectos = [
        asignacion
        for asignacion in asignaciones
        if int(asignacion[1]) == empleado_id
    ]

    if not proyectos:
        print("\nEste empleado no tiene proyectos asignados.")
        print("Primero debes asignarlo a un proyecto.")
        return None

    print("\n========== PROYECTOS ASIGNADOS ==========")
    print(f"{'ID PROYECTO':<15}{'PROYECTO':<30}{'ROL':<20}")
    print("-" * 65)

    for asignacion in proyectos:
        print(
            f"{str(asignacion[3]):<15}"
            f"{str(asignacion[4] or 'Sin asignar'):<30}"
            f"{str(asignacion[5] or 'Sin definir'):<20}"
        )

    print("-" * 65)

    ids_disponibles = list(dict.fromkeys(
        int(asignacion[3]) for asignacion in proyectos
    ))

    if len(ids_disponibles) == 1:
        proyecto_id = ids_disponibles[0]
        print(
            f"Solo hay un proyecto asignado. "
            f"Se seleccionó el ID {proyecto_id}."
        )
        return proyecto_id

    while True:
        entrada = input(
            "ID del proyecto (CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            print("Selección de proyecto cancelada.")
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            print("Volviendo al menú anterior.")
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del proyecto.")
            continue

        try:
            proyecto_id = int(entrada)

            if proyecto_id in ids_disponibles:
                return proyecto_id

            print("Error: selecciona un proyecto de la tabla.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


# ==================================================
# CRUD DE REGISTROS DE TIEMPO
# ==================================================



def menu_tiempos():
    while True:
        print("\n========== REGISTRO DE TIEMPOS ==========")
        print("1. Registrar tiempo")
        print("2. Consultar registros")
        print("3. Modificar registro")
        print("4. Eliminar registro")
        print("0. Volver")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion in ("CANCELAR", "SALIR"):
            break

        if opcion is None:
            continue

        if opcion == 0:
            break

        # ------------------------------------------
        # REGISTRAR
        # ------------------------------------------
        elif opcion == 1:
            print("\n--- Registrar tiempo trabajado ---")

            empleado_id = seleccionar_empleado_tiempo()

            if empleado_id == "SALIR":
                break

            if empleado_id is None or empleado_id == "CANCELAR":
                continue

            proyecto_id = seleccionar_proyecto_tiempo(empleado_id)

            if proyecto_id == "SALIR":
                break

            if proyecto_id is None or proyecto_id == "CANCELAR":
                continue

            datos = leer_formulario([
                ("fecha", "Fecha (YYYY-MM-DD): ", "fecha", None),
                (
                    "horas",
                    "Horas trabajadas: ",
                    "entero",
                    validar_positivo
                ),
                (
                    "descripcion",
                    "Descripción del trabajo: ",
                    "texto",
                    None
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            print("\n========== RESUMEN DEL REGISTRO ==========")
            print(f"Empleado ID: {empleado_id}")
            print(f"Proyecto ID: {proyecto_id}")
            print(f"Fecha: {datos['fecha']}")
            print(f"Horas: {datos['horas']}")
            print(f"Descripción: {datos['descripcion']}")

            respuesta = confirmar_operacion(
                "¿Confirma que desea guardar este registro?"
            )

            if respuesta == "SALIR":
                break

            if respuesta == "CANCELAR":
                continue

            if respuesta is True:
                registro = RegistroTiempo(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    fecha=datos["fecha"],
                    horas=datos["horas"],
                    descripcion=datos["descripcion"]
                )
                GestionTiempo.insertar(registro)

        # ------------------------------------------
        # CONSULTAR
        # ------------------------------------------
        elif opcion == 2:
            print("\n--- Registros de tiempo ---")
            mostrar_registros_tiempo()

        # ------------------------------------------
        # MODIFICAR
        # ------------------------------------------
        elif opcion == 3:
            print("\n--- Modificar registro de tiempo ---")

            registros = mostrar_registros_tiempo()

            if not registros:
                continue

            ids_disponibles = [
                int(registro[0]) for registro in registros
            ]

            registro_id = seleccionar_id(
                "ID del registro que deseas modificar: ",
                ids_disponibles
            )

            if registro_id == "SALIR":
                break

            if registro_id in (None, "CANCELAR"):
                continue

            empleado_id = seleccionar_empleado_tiempo()

            if empleado_id == "SALIR":
                break

            if empleado_id is None or empleado_id == "CANCELAR":
                continue

            proyecto_id = seleccionar_proyecto_tiempo(empleado_id)

            if proyecto_id == "SALIR":
                break

            if proyecto_id is None or proyecto_id == "CANCELAR":
                continue

            datos = leer_formulario([
                ("fecha", "Nueva fecha (YYYY-MM-DD): ", "fecha", None),
                (
                    "horas",
                    "Nuevas horas trabajadas: ",
                    "entero",
                    validar_positivo
                ),
                (
                    "descripcion",
                    "Nueva descripción: ",
                    "texto",
                    None
                ),
            ])

            if datos == "SALIR":
                break

            if datos == "CANCELAR":
                continue

            print("\n========== RESUMEN DE LA MODIFICACIÓN ==========")
            print(f"ID del registro: {registro_id}")
            print(f"Empleado ID: {empleado_id}")
            print(f"Proyecto ID: {proyecto_id}")
            print(f"Fecha: {datos['fecha']}")
            print(f"Horas: {datos['horas']}")
            print(f"Descripción: {datos['descripcion']}")

            respuesta = confirmar_operacion(
                "¿Confirma que desea guardar los cambios?"
            )

            if respuesta == "SALIR":
                break

            if respuesta == "CANCELAR":
                continue

            if respuesta is True:
                registro = RegistroTiempo(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    fecha=datos["fecha"],
                    horas=datos["horas"],
                    descripcion=datos["descripcion"],
                    user_id=registro_id
                )
                GestionTiempo.modificar(registro)

        # ------------------------------------------
        # ELIMINAR
        # ------------------------------------------
        elif opcion == 4:
            print("\n--- Eliminar registro de tiempo ---")

            registros = mostrar_registros_tiempo()

            if not registros:
                continue

            ids_disponibles = [
                int(registro[0]) for registro in registros
            ]

            registro_id = seleccionar_id(
                "ID del registro que deseas eliminar: ",
                ids_disponibles
            )

            if registro_id == "SALIR":
                break

            if registro_id in (None, "CANCELAR"):
                continue

            respuesta = confirmar_eliminacion()

            if respuesta == "SALIR":
                break

            if respuesta is True:
                GestionTiempo.eliminar(registro_id)

        else:
            print("Error: opción no válida.")


def seleccionar_id(mensaje, ids_disponibles):
    while True:
        entrada = input(
            f"{mensaje} (CANCELAR o SALIR para volver): "
        ).strip()

        if entrada.upper() == "CANCELAR":
            return "CANCELAR"

        if entrada.upper() == "SALIR":
            return "SALIR"

        if entrada == "<<":
            print("Estás en la selección del ID.")
            continue

        try:
            identificador = int(entrada)

            if identificador in ids_disponibles:
                return identificador

            print("Error: selecciona un ID de la tabla.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


# ==================================================
# MENÚ PRINCIPAL
# ==================================================


def menu():
    while True:
        print("\n========== SISTEMA ECOTECH ==========")
        print("1. Gestión de empleados")
        print("2. Gestión de departamentos")
        print("3. Gestión de proyectos")
        print("4. Asignación de empleados a proyectos")
        print("5. Registro de tiempos")
        print("0. Salir")

        opcion = leer_entero("Seleccione una opción: ")

        if opcion in ("CANCELAR", "SALIR"):
            print("Volviendo al menú principal.")

            if opcion == "SALIR":
                print("Hasta luego.")
                break

            continue

        if opcion is None:
            continue

        if opcion == 0:
            print("Hasta luego.")
            break

        elif opcion == 1:
            menu_empleados()

        elif opcion == 2:
            menu_departamentos()

        elif opcion == 3:
            menu_proyectos()

        elif opcion == 4:
            menu_asignaciones()

        elif opcion == 5:
            menu_tiempos()

        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    menu()
