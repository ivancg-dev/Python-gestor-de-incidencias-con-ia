from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from collections import Counter
import matplotlib.pyplot as plt
from database.database import (
    get_incidencias, add_incidencia, delete_incidencia,
    get_titulos_y_estados, update_estado_incidencia
)
from windows.ficheroincidencias import IncidenciaForm

class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestor de Incidencias")
        self.resize(800, 450)

        layout = QVBoxLayout()

        # Filtros
        filtros_container = QWidget()
        filtros_layout = QHBoxLayout()
        filtros_layout.setContentsMargins(20, 20, 20, 10)
        filtros_layout.setSpacing(10)

        filtros_izquierda = QHBoxLayout()
        label_estado = QLabel("Estado:")
        label_estado.setMinimumWidth(50)
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Todos", "pendiente", "cerrado"])
        self.estado_combo.setFixedWidth(110)

        label_prioridad = QLabel("Prioridad:")
        label_prioridad.setMinimumWidth(60)
        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(["Todos", "baja", "media", "alta", "extrema"])
        self.prioridad_combo.setFixedWidth(110)

        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_filtrar.setFixedWidth(90)
        self.boton_filtrar.clicked.connect(self.load_data)

        filtros_izquierda.addWidget(label_estado)
        filtros_izquierda.addWidget(self.estado_combo)
        filtros_izquierda.addSpacing(15)
        filtros_izquierda.addWidget(label_prioridad)
        filtros_izquierda.addWidget(self.prioridad_combo)
        filtros_izquierda.addSpacing(10)
        filtros_izquierda.addWidget(self.boton_filtrar)

        filtros_derecha = QHBoxLayout()
        self.boton_graficas = QPushButton("Gráficas")
        self.boton_graficas.setFixedWidth(100)
        self.boton_graficas.clicked.connect(self.mostrar_grafica_estado)
        filtros_derecha.addStretch()
        filtros_derecha.addWidget(self.boton_graficas)

        filtros_layout.addLayout(filtros_izquierda)
        filtros_layout.addStretch()
        filtros_layout.addLayout(filtros_derecha)

        filtros_container.setLayout(filtros_layout)
        layout.addWidget(filtros_container)
        layout.addSpacing(10)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título", "Descripción", "Categoría", "Estado", "Prioridad", "Fecha creación"
        ])
        layout.addWidget(self.table)
        layout.addSpacing(10)

        # Acciones
        acciones = QHBoxLayout()
        self.btn_add = QPushButton("Agregar")
        self.btn_add.clicked.connect(self.show_incidencias)

        self.btn_toggle_estado = QPushButton("Cambiar estado")
        self.btn_toggle_estado.clicked.connect(self.toggle_estado)

        self.btn_delete = QPushButton("Eliminar seleccionada")
        self.btn_delete.clicked.connect(self.delete_incidencia)

        acciones.addWidget(self.btn_add)
        acciones.addWidget(self.btn_toggle_estado)
        acciones.addWidget(self.btn_delete)

        layout.addLayout(acciones)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        estado = self.estado_combo.currentText()
        prioridad = self.prioridad_combo.currentText()
        incidencias = get_incidencias(estado, prioridad)
        self.table.setRowCount(len(incidencias))

        for row, inc in enumerate(incidencias):
            for col, valor in enumerate(inc):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def add_incidencia(self):
        titulo = self.titulo_input.text()
        descripcion = self.descripcion_input.text()
        categoria = self.categoria_input.text()
        estado = self.estado_nuevo.currentText()
        prioridad = self.prioridad_nueva.currentText()

        if titulo.strip() and categoria.strip():
            add_incidencia(titulo, descripcion, categoria, estado, prioridad, self.user_id)
            self.load_data()
            self.titulo_input.clear()
            self.descripcion_input.clear()
            self.categoria_input.clear()

    def delete_incidencia(self):
        fila = self.table.currentRow()
        if fila >= 0:
            incidencia_id = int(self.table.item(fila, 0).text())
            delete_incidencia(incidencia_id)
            self.load_data()
            QMessageBox.information(self, "Eliminación exitosa", "La incidencia ha sido eliminada correctamente.")
        else:
            QMessageBox.warning(self, "Sin selección", "Por favor, selecciona una incidencia para eliminar.")

    def toggle_estado(self):
        fila = self.table.currentRow()
        if fila >= 0:
            incidencia_id = int(self.table.item(fila, 0).text())
            estado_actual = self.table.item(fila, 4).text()
            nuevo_estado = "cerrado" if estado_actual == "pendiente" else "pendiente"
            update_estado_incidencia(incidencia_id, nuevo_estado)
            self.load_data()
            QMessageBox.information(self, "Estado actualizado", f"Estado cambiado a '{nuevo_estado}'.")
        else:
            QMessageBox.warning(self, "Sin selección", "Selecciona una incidencia para cambiar su estado.")

    def show_incidencias(self):
        self.ficheroincidencias = IncidenciaForm(self.user_id)
        self.ficheroincidencias.incidencia_registrada.connect(self.load_data)
        self.ficheroincidencias.show()

    def mostrar_grafica_estado(self):
        datos = get_titulos_y_estados()
        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return

        estados = [estado for _, estado in datos]
        conteo_estados = Counter(estados)
        etiquetas, valores = zip(*sorted(conteo_estados.items(), key=lambda x: x[1], reverse=True))

        colores = plt.get_cmap('Set3').colors
        plt.figure(figsize=(6, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
        plt.title('Distribución de Incidencias por Estado')
        plt.axis('equal')
        plt.show()