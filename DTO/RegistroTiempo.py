class RegistroTiempo:

    def __init__(
        self,
        empleado_id,
        proyecto_id,
        fecha,
        horas,
        descripcion,
        user_id=None
    ):
        self.user_id = user_id
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Empleado: {self.empleado_id} | "
            f"Proyecto: {self.proyecto_id} | "
            f"Fecha: {self.fecha} | "
            f"Horas: {self.horas} | "
            f"Descripción: {self.descripcion}"
        )