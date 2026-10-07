class AsignacionEmp:

    def __init__(
        self,
        empleado_id,
        proyecto_id,
        rol,
        asignacion_id=None
    ):
        self.asignacion_id = asignacion_id
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.rol = rol

    def __str__(self):
        return (
            f"ID Asignación: {self.asignacion_id} | "
            f"Empleado: {self.empleado_id} | "
            f"Proyecto: {self.proyecto_id} | "
            f"Rol: {self.rol}"
        )