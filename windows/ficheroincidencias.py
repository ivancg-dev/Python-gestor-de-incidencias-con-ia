from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class IncidenciaForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar Incidencia")
        self.setFixedSize(600, 500)

        '''Título principal'''
        titulo_label = QLabel("Formulario de Incidencia")
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(20)
        fuente_titulo.setBold(True)
        titulo_label.setFont(fuente_titulo)
        titulo_label.setAlignment(Qt.AlignCenter)

        '''Campos de entrada'''
        label_titulo = QLabel("Título:")
        input_titulo = QLineEdit()
        input_titulo.setFixedHeight(30)

        label_descripcion = QLabel("Descripción:")
        input_descripcion = QTextEdit()
        input_descripcion.setFixedHeight(80)

        label_categoria = QLabel("Categoría:")
        input_categoria = QLineEdit()
        input_categoria.setFixedHeight(30)

        label_estado = QLabel("Estado:")
        input_estado = QComboBox()
        input_estado.addItems(["pendiente", "cerrado"])

        label_prioridad = QLabel("Prioridad:")
        input_prioridad = QComboBox()
        input_prioridad.addItems(["baja", "media", "alta", "extrema"])

        label_usuario_id = QLabel("ID de Usuario:")
        input_usuario_id = QLineEdit()
        input_usuario_id.setFixedHeight(30)

        '''Botón de envío'''
        boton_enviar = QPushButton("Registrar Incidencia")
        boton_enviar.setFixedSize(200, 40)

        '''Layouts'''
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(titulo_label)
        layout_principal.addSpacing(30)

        layout_principal.addWidget(label_titulo)
        layout_principal.addWidget(input_titulo)

        layout_principal.addWidget(label_descripcion)
        layout_principal.addWidget(input_descripcion)

        layout_principal.addWidget(label_categoria)
        layout_principal.addWidget(input_categoria)

        layout_principal.addWidget(label_estado)
        layout_principal.addWidget(input_estado)

        layout_principal.addWidget(label_prioridad)
        layout_principal.addWidget(input_prioridad)

        layout_principal.addWidget(label_usuario_id)
        layout_principal.addWidget(input_usuario_id)

        layout_principal.addStretch()
        layout_principal.addWidget(boton_enviar, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)