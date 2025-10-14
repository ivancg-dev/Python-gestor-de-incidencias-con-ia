from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from database.database import add_incidencia

# ✅ Importamos la función de predicción desde el módulo IA
from resources.IA import predecir_categoria


class IncidenciaForm(QDialog):
    incidencia_registrada = pyqtSignal()  # ← señal para notificar que se ha registrado

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Registrar Incidencia")
        self.setFixedSize(600, 500)

        # --- Campos ---
        self.input_titulo = QLineEdit()
        self.input_descripcion = QTextEdit()
        self.input_descripcion.textChanged.connect(self.actualizar_categoria)  # ← IA en tiempo real

        # --- Etiqueta de categoría dinámica ---
        self.label_prediccion = QLabel("Categoría estimada: leve")
        self.label_prediccion.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_prediccion.setStyleSheet("color: green;")

        # --- Categoría como ComboBox ---
        self.input_categoria = QComboBox()
        self.input_categoria.addItems(["leve", "medio", "grave", "extremo"])

        self.input_estado = QComboBox()
        self.input_estado.addItems(["pendiente", "cerrado"])

        self.input_prioridad = QComboBox()
        self.input_prioridad.addItems(["baja", "media", "alta", "extrema"])

        boton_enviar = QPushButton("Registrar Incidencia")
        boton_enviar.clicked.connect(self.registrar_incidencia)

        # --- Layout principal ---
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.input_titulo)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)

        # Línea con la etiqueta dinámica
        layout_pred = QHBoxLayout()
        layout_pred.addWidget(self.label_prediccion)
        layout.addLayout(layout_pred)

        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.input_categoria)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.input_estado)
        layout.addWidget(QLabel("Prioridad:"))
        layout.addWidget(self.input_prioridad)
        layout.addWidget(boton_enviar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    # =====================================================
    # === FUNCIÓN QUE ACTUALIZA LA CATEGORÍA EN TIEMPO REAL
    # =====================================================
    def actualizar_categoria(self):
        texto = self.input_descripcion.toPlainText().strip()
        categoria_predicha = predecir_categoria(texto)

        # Actualizar comboBox
        index = self.input_categoria.findText(categoria_predicha)
        if index != -1:
            self.input_categoria.setCurrentIndex(index)

        # Cambiar color y texto del label
        colores = {
            "leve": "green",
            "medio": "orange",
            "grave": "red",
            "extremo": "darkred"
        }
        color = colores.get(categoria_predicha, "black")
        self.label_prediccion.setText(f"Categoría estimada: {categoria_predicha}")
        self.label_prediccion.setStyleSheet(f"color: {color};")

    # =====================================================
    # === FUNCIÓN PARA GUARDAR LA INCIDENCIA EN LA BD
    # =====================================================
    def registrar_incidencia(self):
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.toPlainText().strip()
        categoria = self.input_categoria.currentText()
        estado = self.input_estado.currentText()
        prioridad = self.input_prioridad.currentText()
        usuario_id = self.user_id

        if not (titulo and categoria):
            QMessageBox.warning(self, "Error", "Título y Categoría son obligatorios.")
            return

        try:
            usuario_id = int(usuario_id)
        except ValueError:
            QMessageBox.warning(self, "Error", "El ID de usuario debe ser un número.")
            return

        add_incidencia(titulo, descripcion, categoria, estado, prioridad, usuario_id)
        QMessageBox.information(self, "Éxito", "Incidencia registrada correctamente.")
        self.incidencia_registrada.emit()  # ← emitimos la señal
        self.accept()  # ← cerramos la ventana
