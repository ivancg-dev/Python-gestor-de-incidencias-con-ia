from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from database.database import add_incidencia

class IncidenciaForm(QDialog):
    incidencia_registrada = pyqtSignal()  # ← señal para notificar que se ha registrado

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Incidencia")
        self.setFixedSize(600, 500)

        # Campos
        self.input_titulo = QLineEdit()
        self.input_descripcion = QTextEdit()
        self.input_categoria = QLineEdit()
        self.input_estado = QComboBox()
        self.input_estado.addItems(["pendiente", "cerrado"])
        self.input_prioridad = QComboBox()
        self.input_prioridad.addItems(["baja", "media", "alta", "extrema"])
        self.input_usuario_id = QLineEdit()

        boton_enviar = QPushButton("Registrar Incidencia")
        boton_enviar.clicked.connect(self.registrar_incidencia)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.input_titulo)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.input_categoria)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.input_estado)
        layout.addWidget(QLabel("Prioridad:"))
        layout.addWidget(self.input_prioridad)
        layout.addWidget(QLabel("ID de Usuario:"))
        layout.addWidget(self.input_usuario_id)
        layout.addWidget(boton_enviar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def registrar_incidencia(self):
        titulo = self.input_titulo.text().strip()
        descripcion = self.input_descripcion.toPlainText().strip()
        categoria = self.input_categoria.text().strip()
        estado = self.input_estado.currentText()
        prioridad = self.input_prioridad.currentText()
        usuario_id = self.input_usuario_id.text().strip()

        if not (titulo and categoria and usuario_id):
            QMessageBox.warning(self, "Error", "Título, Categoría y Usuario ID son obligatorios.")
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