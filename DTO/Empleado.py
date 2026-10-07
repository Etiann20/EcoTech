from DTO.Persona import Persona


class Empleado(Persona):

    def __init__(
        self,
        run,
        nombre,
        direccion,
        telefono,
        correo,
        fecha_inicio,
        salario,
        departamento_id,
        user_id=None
    ):
        super().__init__(
            run,
            nombre,
            direccion,
            telefono,
            correo,
            user_id
        )

        self.fecha_inicio = fecha_inicio
        self.salario = salario
        self.departamento_id = departamento_id

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"RUN: {self.run} | "
            f"Nombre: {self.nombre} | "
            f"Fecha inicio: {self.fecha_inicio} | "
            f"Salario: {self.salario} | "
            f"Departamento: {self.departamento_id}"
        )