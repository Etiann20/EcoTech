class Departamento:

    def __init__(
        self,
        nombre,
        descripcion,
        gerente_empleado_id=None,
        user_id=None
    ):
        self.user_id = user_id
        self.nombre = nombre
        self.gerente_empleado_id = gerente_empleado_id
        self.descripcion = descripcion

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Nombre: {self.nombre} | "
            f"Gerente: {self.gerente_empleado_id} | "
            f"Descripción: {self.descripcion}"
        )