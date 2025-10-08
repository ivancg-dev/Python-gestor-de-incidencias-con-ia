from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
)
from database.database import *


class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestor de Incidencias")
        self.resize(800, 450)

        layout = QVBoxLayout()

        # --- Filtros ---
        filtros = QHBoxLayout()
        filtros.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Todos", "pendiente", "cerrado"])
        filtros.addWidget(self.estado_combo)

        filtros.addWidget(QLabel("Prioridad:"))
        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(["Todos", "baja", "media", "alta", "extrema"])
        filtros.addWidget(self.prioridad_combo)

        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_filtrar.clicked.connect(self.load_data)
        filtros.addWidget(self.boton_filtrar)
        layout.addLayout(filtros)

        # --- Tabla ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título", "Descripción", "Categoría", "Estado", "Prioridad", "Fecha creación"
        ])
        layout.addWidget(self.table)

        # --- Zona de acciones ---
        acciones = QHBoxLayout()
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título")
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción")
        self.categoria_input = QLineEdit()
        self.categoria_input.setPlaceholderText("Categoría")

        self.estado_nuevo = QComboBox()
        self.estado_nuevo.addItems(["pendiente", "cerrado"])

        self.prioridad_nueva = QComboBox()
        self.prioridad_nueva.addItems(["baja", "media", "alta", "extrema"])

        self.btn_add = QPushButton("Agregar")
        self.btn_add.clicked.connect(self.add_incidencia)

        self.btn_delete = QPushButton("Eliminar seleccionada")
        self.btn_delete.clicked.connect(self.delete_incidencia)

        acciones.addWidget(self.titulo_input)
        acciones.addWidget(self.descripcion_input)
        acciones.addWidget(self.categoria_input)
        acciones.addWidget(self.estado_nuevo)
        acciones.addWidget(self.prioridad_nueva)
        acciones.addWidget(self.btn_add)
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
                self.table.setItem(row, col, QTableWidgetItem(str(valor)))

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
