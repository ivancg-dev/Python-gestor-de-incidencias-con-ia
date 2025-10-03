from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class loginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Iniciar sesión")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        # Crear el título con estilo y alinearlo al centro
        label_1 = QLabel("Iniciar sesión")
        titulo_fuente = QFont()
        titulo_fuente.setPointSize(24)
        titulo_fuente.setBold(True)
        label_1.setFont(titulo_fuente)
        label_1.setAlignment(Qt.AlignCenter)

        label_3 = QLabel("tercero label")
        label_4 = QLabel("Usuario:")
        label_5 = QLabel("Contraseña:")
        boton_login = QPushButton("Iniciar sesión")
        boton_singup = QPushButton("Iniciar sesión")



        # Campos de texto
        input_usuario = QLineEdit()
        input_contrasena = QLineEdit()
        input_contrasena.setEchoMode(QLineEdit.Password)  # Oculta el texto

        layout_principal = QVBoxLayout()
        layout_secundario = QVBoxLayout()
        layout_secundario_1 = QVBoxLayout()
        layout_secundario_2 = QVBoxLayout()
        layout_secundario_1_1 = QVBoxLayout()
        layout_secundario_1_2 = QVBoxLayout()
        layout_secundario_2_1 = QVBoxLayout()
        layout_secundario_2_2 = QVBoxLayout()
        layout_terciario = QVBoxLayout()

        layout_principal.addWidget(label_1)
        layout_terciario.addWidget(label_3)

        layout_secundario_1_1.addWidget(label_4)
        layout_secundario_1_2.addWidget(input_usuario)
        layout_secundario_2_1.addWidget(label_5)
        layout_secundario_2_2.addWidget(input_contrasena)
        layout_terciario.addWidget(boton_login)

        layout_principal.addLayout(layout_secundario)
        layout_principal.addLayout(layout_terciario)
        layout_secundario.addLayout(layout_secundario_1)
        layout_secundario.addLayout(layout_secundario_2)
        layout_secundario.addLayout(layout_secundario_1_1)
        layout_secundario.addLayout(layout_secundario_1_2)
        layout_secundario.addLayout(layout_secundario_2_1)
        layout_secundario.addLayout(layout_secundario_2_2)

        self.setLayout(layout_principal)