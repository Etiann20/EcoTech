class Proyecto:

    def __init__(
        self,
        nombre,
        descripcion,
        fecha_inicio,
        user_id=None
    ):
        self.user_id = user_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Nombre: {self.nombre} | "
            f"Descripción: {self.descripcion} | "
            f"Fecha inicio: {self.fecha_inicio}"
        )