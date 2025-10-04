from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class loginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Iniciar sesión")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        '''
        Título
        '''

        label_1 = QLabel("Iniciar sesión")
        titulo_fuente = QFont()
        titulo_fuente.setPointSize(24)
        titulo_fuente.setBold(True)
        label_1.setFont(titulo_fuente)
        label_1.setAlignment(Qt.AlignCenter)

        '''
        Labels
        '''

        label_2 = QLabel("Usuario:")
        label_3 = QLabel("Contraseña:")

        '''
        Campos de texto más grandes
        '''

        input_usuario = QLineEdit()
        input_usuario.setFixedHeight(40)
        input_usuario.setMinimumWidth(300)

        input_contrasena = QLineEdit()
        '''Hacemos que en el QLineEdit no se vea lo que se escribe, solo se ven puntos'''
        input_contrasena.setEchoMode(QLineEdit.Password)
        input_contrasena.setFixedHeight(40)
        input_contrasena.setMinimumWidth(300)

        '''Botones más grandes'''
        boton_login = QPushButton("Iniciar sesión")
        boton_login.setFixedSize(150, 40)

        boton_singup = QPushButton("Registrarse")
        boton_singup.setFixedSize(150, 40)

        '''Layouts'''
        layout_principal = QVBoxLayout()
        layout_secundario = QVBoxLayout()
        layout_secundario_1_1 = QHBoxLayout()
        layout_secundario_2_1 = QHBoxLayout()
        layout_botones = QHBoxLayout()

        layout_principal.addWidget(label_1)
        '''addSpacing son espacio entre título y campos'''
        layout_principal.addSpacing(40)  


        layout_secundario_1_1.addWidget(label_2)
        layout_secundario_1_1.addWidget(input_usuario)
        layout_secundario_2_1.addWidget(label_3)
        layout_secundario_2_1.addWidget(input_contrasena)

        layout_botones.addWidget(boton_login)
        layout_botones.addStretch()
        '''addStrech lleva el segundo botón al otro extremo'''
        layout_botones.addWidget(boton_singup)

        layout_secundario.addLayout(layout_secundario_1_1)
        layout_secundario.addSpacing(20)
        layout_secundario.addLayout(layout_secundario_2_1)

        layout_principal.addLayout(layout_secundario)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)