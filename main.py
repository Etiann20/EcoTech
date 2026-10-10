from datetime import datetime

from DTO.Departamento import Departamento
from DTO.Empleado import Empleado
from DTO.Proyecto import Proyecto
from DTO.AsignacionEmp import AsignacionEmp

from DAO import GestionDepartamento
from DAO import GestionEmpleado
from DAO import GestionProyecto
from DAO import GestionAsignacion


# ==================================================
# FUNCIONES PARA VALIDAR DATOS
# ==================================================

def leer_texto(mensaje):
    while True:
        try:
            texto = input(mensaje).strip()

            if not texto:
                raise ValueError("El campo no puede estar vacío.")

            return texto

        except ValueError as e:
            print("Error:", e)


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje).strip())

        except ValueError:
            print("Error: debes ingresar un número entero.")


def leer_fecha(mensaje):
    while True:
        try:
            fecha_texto = input(mensaje).strip()
            return datetime.strptime(fecha_texto, "%Y-%m-%d").date()

        except ValueError:
            print("Error: usa una fecha válida con formato YYYY-MM-DD.")


# ==================================================
# CONFIRMACIONES
# ==================================================

def confirmar_eliminacion():
    while True:
        respuesta = input(
            "¿Está realmente seguro que quiere eliminar? (sí/no): "
        ).strip().lower()

        if respuesta in ("si", "sí", "s"):
            return True

        elif respuesta in ("no", "n"):
            print("Eliminación cancelada.")
            return False

        else:
            print("Respuesta no válida. Escribe sí o no.")


def confirmar_asignacion(accion="registrar"):
    while True:
        respuesta = input(
            f"¿Está realmente seguro que quiere {accion} "
            "esta asignación? (sí/no): "
        ).strip().lower()

        if respuesta in ("si", "sí", "s"):
            return True

        elif respuesta in ("no", "n"):
            print("Operación cancelada.")
            return False

        else:
            print("Respuesta no válida. Escribe sí o no.")


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
        departamento_id = leer_entero("ID del departamento: ")

        if departamento_id in ids_disponibles:
            return departamento_id

        print("Error: selecciona un ID de departamento existente.")


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

        if opcion == 0:
            break

        elif opcion == 1:
            print("\n--- Registrar departamento ---")

            nombre = leer_texto("Nombre: ")
            descripcion = leer_texto("Descripción: ")

            departamento = Departamento(
                nombre=nombre,
                descripcion=descripcion
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

            user_id = leer_entero(
                "ID del departamento que deseas modificar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el departamento no existe.")
                continue

            nombre = leer_texto("Nuevo nombre: ")
            descripcion = leer_texto("Nueva descripción: ")

            gerente_id = next(
                fila[2]
                for fila in departamentos
                if fila[0] == user_id
            )

            departamento = Departamento(
                nombre=nombre,
                descripcion=descripcion,
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

            user_id = leer_entero(
                "ID del departamento que deseas eliminar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el departamento no existe.")
                continue

            if confirmar_eliminacion():
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

        if opcion == 0:
            break

        elif opcion == 1:
            print("\n--- Registrar empleado ---")

            departamento_id = seleccionar_departamento()

            if departamento_id is None:
                continue

            run = leer_texto("RUN: ")
            nombre = leer_texto("Nombre: ")
            direccion = leer_texto("Dirección: ")
            telefono = leer_entero("Teléfono (solo números): ")
            correo = leer_texto("Correo: ")
            fecha_inicio = leer_fecha(
                "Fecha de inicio (YYYY-MM-DD): "
            )
            salario = leer_entero("Salario: ")

            if salario < 0:
                print("Error: el salario no puede ser negativo.")
                continue

            empleado = Empleado(
                run=run,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
                fecha_inicio=fecha_inicio,
                salario=salario,
                departamento_id=departamento_id
            )

            GestionEmpleado.insertar(empleado)

        elif opcion == 2:
            print("\n--- Empleados registrados ---")
            mostrar_empleados()

        elif opcion == 3:
            print("\n--- Modificar empleado ---")

            empleados = mostrar_empleados()

            if not empleados:
                continue

            ids_disponibles = [fila[0] for fila in empleados]

            user_id = leer_entero(
                "ID del empleado que deseas modificar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el empleado no existe.")
                continue

            departamento_id = seleccionar_departamento()

            if departamento_id is None:
                continue

            run = leer_texto("Nuevo RUN: ")
            nombre = leer_texto("Nuevo nombre: ")
            direccion = leer_texto("Nueva dirección: ")
            telefono = leer_entero(
                "Nuevo teléfono (solo números): "
            )
            correo = leer_texto("Nuevo correo: ")
            fecha_inicio = leer_fecha(
                "Nueva fecha de inicio (YYYY-MM-DD): "
            )
            salario = leer_entero("Nuevo salario: ")

            if salario < 0:
                print("Error: el salario no puede ser negativo.")
                continue

            empleado = Empleado(
                run=run,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
                fecha_inicio=fecha_inicio,
                salario=salario,
                departamento_id=departamento_id,
                user_id=user_id
            )

            GestionEmpleado.modificar(empleado)

        elif opcion == 4:
            print("\n--- Eliminar empleado ---")

            empleados = mostrar_empleados()

            if not empleados:
                continue

            ids_disponibles = [fila[0] for fila in empleados]

            user_id = leer_entero(
                "ID del empleado que deseas eliminar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el empleado no existe.")
                continue

            if confirmar_eliminacion():
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

        if opcion == 0:
            break

        elif opcion == 1:
            print("\n--- Registrar proyecto ---")

            nombre = leer_texto("Nombre: ")
            descripcion = leer_texto("Descripción: ")
            fecha_inicio = leer_fecha(
                "Fecha de inicio (YYYY-MM-DD): "
            )

            proyecto = Proyecto(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio
            )

            GestionProyecto.insertar(proyecto)

        elif opcion == 2:
            print("\n--- Proyectos registrados ---")
            mostrar_proyectos()

        elif opcion == 3:
            print("\n--- Modificar proyecto ---")

            proyectos = mostrar_proyectos()

            if not proyectos:
                continue

            ids_disponibles = [fila[0] for fila in proyectos]

            user_id = leer_entero(
                "ID del proyecto que deseas modificar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el proyecto no existe.")
                continue

            nombre = leer_texto("Nuevo nombre: ")
            descripcion = leer_texto("Nueva descripción: ")
            fecha_inicio = leer_fecha(
                "Nueva fecha de inicio (YYYY-MM-DD): "
            )

            proyecto = Proyecto(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                user_id=user_id
            )

            GestionProyecto.modificar(proyecto)

        elif opcion == 4:
            print("\n--- Eliminar proyecto ---")

            proyectos = mostrar_proyectos()

            if not proyectos:
                continue

            ids_disponibles = [fila[0] for fila in proyectos]

            user_id = leer_entero(
                "ID del proyecto que deseas eliminar: "
            )

            if user_id not in ids_disponibles:
                print("Error: el proyecto no existe.")
                continue

            if confirmar_eliminacion():
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
        empleado_id = leer_entero("Ingrese el ID del empleado: ")

        if empleado_id in ids_disponibles:
            empleado = next(
                fila for fila in empleados if fila[0] == empleado_id
            )
            return empleado_id, empleado[2]

        print("Error: ese ID de empleado no existe.")
        print("Selecciona uno de los IDs mostrados en la tabla.")


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
        proyecto_id = leer_entero("Ingrese el ID del proyecto: ")

        if proyecto_id in ids_disponibles:
            proyecto = next(
                fila for fila in proyectos if fila[0] == proyecto_id
            )
            return proyecto_id, proyecto[1]

        print("Error: ese ID de proyecto no existe.")
        print("Selecciona uno de los IDs mostrados en la tabla.")


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

        if opcion == 0:
            break

        elif opcion == 1:
            print("\n--- Registrar asignación ---")

            empleado_seleccionado = seleccionar_empleado_asignacion()

            if empleado_seleccionado is None:
                continue

            empleado_id, empleado_nombre = empleado_seleccionado

            proyecto_seleccionado = seleccionar_proyecto_asignacion()

            if proyecto_seleccionado is None:
                continue

            proyecto_id, proyecto_nombre = proyecto_seleccionado
            rol = leer_texto("Rol del empleado en el proyecto: ")

            print("\n========== RESUMEN DE LA ASIGNACIÓN ==========")
            print(f"ID empleado: {empleado_id}")
            print(f"Empleado:    {empleado_nombre}")
            print(f"ID proyecto: {proyecto_id}")
            print(f"Proyecto:    {proyecto_nombre}")
            print(f"Rol:         {rol}")
            print("=" * 48)

            if confirmar_asignacion("registrar"):
                asignacion = AsignacionEmp(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    rol=rol
                )
                GestionAsignacion.insertar(asignacion)

        elif opcion == 2:
            print("\n--- Asignaciones registradas ---")
            mostrar_asignaciones()

        elif opcion == 3:
            print("\n--- Modificar asignación ---")

            asignaciones = mostrar_asignaciones()

            if not asignaciones:
                continue

            ids_disponibles = [fila[0] for fila in asignaciones]

            asignacion_id = leer_entero(
                "ID de la asignación que deseas modificar: "
            )

            if asignacion_id not in ids_disponibles:
                print("Error: la asignación no existe.")
                continue

            empleado_seleccionado = seleccionar_empleado_asignacion()

            if empleado_seleccionado is None:
                continue

            empleado_id, empleado_nombre = empleado_seleccionado

            proyecto_seleccionado = seleccionar_proyecto_asignacion()

            if proyecto_seleccionado is None:
                continue

            proyecto_id, proyecto_nombre = proyecto_seleccionado
            rol = leer_texto("Nuevo rol: ")

            print("\n========== RESUMEN DE LA MODIFICACIÓN ==========")
            print(f"ID asignación: {asignacion_id}")
            print(f"Empleado:      {empleado_nombre} (ID: {empleado_id})")
            print(f"Proyecto:      {proyecto_nombre} (ID: {proyecto_id})")
            print(f"Nuevo rol:     {rol}")
            print("=" * 50)

            if confirmar_asignacion("modificar"):
                asignacion = AsignacionEmp(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    rol=rol,
                    asignacion_id=asignacion_id
                )
                GestionAsignacion.modificar(asignacion)

        elif opcion == 4:
            print("\n--- Eliminar asignación ---")

            asignaciones = mostrar_asignaciones()

            if not asignaciones:
                continue

            ids_disponibles = [fila[0] for fila in asignaciones]

            asignacion_id = leer_entero(
                "ID de la asignación que deseas eliminar: "
            )

            if asignacion_id not in ids_disponibles:
                print("Error: la asignación no existe.")
                continue

            if confirmar_eliminacion():
                GestionAsignacion.eliminar(asignacion_id)

        else:
            print("Error: opción no válida.")


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
            print("El módulo de registro de tiempos está pendiente.")

        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    menu()