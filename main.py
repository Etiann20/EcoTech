from datetime import datetime
from DAO import GestionDepartamento
from DTO.Departamento import Departamento

def leer_texto(mensaje):
    while True:
        try:
            texto = input(mensaje).strip()

            if texto == "":
                raise ValueError("El campo no puede estar vacío.")

            return texto

        except ValueError as e:
            print("Error:", e)


def leer_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            return numero

        except ValueError:
            print("Error: debes ingresar un número entero.")


def leer_float(mensaje):
    while True:
        try:
            numero = float(input(mensaje))
            return numero

        except ValueError:
            print("Error: debes ingresar un número válido.")


def leer_fecha(mensaje):
    while True:
        try:
            fecha = input(mensaje)

            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

            return fecha

        except ValueError:
            print("Error: usa el formato YYYY-MM-DD.")


def menu():
    while True:
        print("\n========== ECOTECH ==========")
        print("1. Gestionar empleados")
        print("2. Gestionar departamentos")
        print("3. Gestionar proyectos")
        print("4. Gestionar asignaciones")
        print("5. Gestionar registros de tiempo")
        print("0. Salir")
        print("==============================")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 0:
                print("Programa finalizado.")
                break

            elif opcion == 1:
                print("Gestión de empleados")

            elif opcion == 2:
                menu_departamentos()

            elif opcion == 3:
                print("Gestión de proyectos")

            elif opcion == 4:
                print("Gestión de asignaciones")

            elif opcion == 5:
                print("Gestión de registros de tiempo")

            else:
                print("Error: opción no válida.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


def menu_departamentos():

    while True:
        print("\n===== GESTIÓN DE DEPARTAMENTOS =====")
        print("1. Registrar departamento")
        print("2. Consultar departamentos")
        print("3. Modificar departamento")
        print("4. Eliminar departamento")
        print("0. Volver")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 0:
                break

            elif opcion == 1:
                print("\n--- Registrar departamento ---")

                nombre = leer_texto("Nombre: ")
                descripcion = leer_texto("Descripción: ")

                departamento = Departamento(
                    nombre,
                    descripcion
                )

                GestionDepartamento.insertar(departamento)

            elif opcion == 2:
                print("\n--- Departamentos registrados ---")
                GestionDepartamento.consultar()

            elif opcion == 3:
                print("\n--- Modificar departamento ---")

                user_id = leer_entero("ID del departamento: ")
                nombre = leer_texto("Nuevo nombre: ")
                descripcion = leer_texto("Nueva descripción: ")

                departamento = Departamento(
                    nombre,
                    descripcion,
                    user_id=user_id
                )

                GestionDepartamento.modificar(departamento)

            elif opcion == 4:
                print("\n--- Eliminar departamento ---")

                user_id = leer_entero("ID del departamento: ")

                GestionDepartamento.eliminar(user_id)

            else:
                print("Error: opción no válida.")

        except ValueError:
            print("Error: debes ingresar un número entero.")


menu()
