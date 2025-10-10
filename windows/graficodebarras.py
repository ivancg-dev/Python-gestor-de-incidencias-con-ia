import matplotlib.pyplot as plt
from database import get_titulos_y_prioridades

datos = get_titulos_y_prioridades()
# Si no hay incidencias, evitar error
if not datos:
    print("No hay incidencias registradas.")
else:
    # Separar títulos y prioridades
    titulos = [fila[0] for fila in datos]
    prioridades = [fila[1] for fila in datos]

    # Convertir prioridades a valores numéricos (para el gráfico)
    prioridad_valores = {
        "baja": 1,
        "media": 2,
        "alta": 3,
        "extrema": 4
    }
    valores = [prioridad_valores.get(p, 0) for p in prioridades]

    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(titulos, valores, color="skyblue")
    plt.title("Prioridad de Incidencias")
    plt.xlabel("Título de la incidencia")
    plt.ylabel("Nivel de prioridad (1=baja, 4=extrema)")
    plt.xticks(rotation=45, ha="right")

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()
