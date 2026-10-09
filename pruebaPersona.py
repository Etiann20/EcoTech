
from DTO.RegistroTiempo import RegistroTiempo

registro = RegistroTiempo(
    empleado_id=1,
    proyecto_id=1,
    fecha="2026-10-08",
    horas=8,
    descripcion="Trabajo en el proyecto"
)

print(registro)
print("Horas:", registro.horas)
print("Descripción:", registro.descripcion)
