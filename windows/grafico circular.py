import matplotlib.pyplot as plt
from database import get_titulos_y_estados
from collections import Counter

# Obtener datos desde la base de datos
datos = get_titulos_y_estados()

# Contar cuántas veces aparece cada estado
estados = [estado for _, estado in datos]
conteo_estados = Counter(estados)

# Extraer etiquetas y valores
etiquetas = list(conteo_estados.keys())
valores = list(conteo_estados.values())

# Crear gráfico de pastel
plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)

# Establecer el título del gráfico
plt.title('Distribución de Incidencias por Estado')

# Asegurar que sea circular
plt.axis('equal')

# Mostrar gráfico
plt.show()
