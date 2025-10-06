from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class RegistroDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de usuario")
        self.setFixedSize(400, 300)

        '''Título de la ventana de registro'''
        titulo = QLabel("Crear cuenta")
        fuente = QFont()
        fuente.setPointSize(20)
        fuente.setBold(True)
        titulo.setFont(fuente)
        titulo.setAlignment(Qt.AlignCenter)

        '''Campos de entrada'''
        label_usuario = QLabel("Nuevo usuario:")
        input_usuario = QLineEdit()

        label_contrasena = QLabel("Nueva contraseña:")
        input_contrasena = QLineEdit()
        input_contrasena.setEchoMode(QLineEdit.Password)

        '''Botones de acción'''
        boton_registrar = QPushButton("Registrar")
        boton_cancelar = QPushButton("Cancelar")
        

        '''Layouts para organizar los elementos'''
        layout_usuario = QHBoxLayout()
        layout_usuario.addWidget(label_usuario)
        layout_usuario.addWidget(input_usuario)

        layout_contrasena = QHBoxLayout()
        layout_contrasena.addWidget(label_contrasena)
        layout_contrasena.addWidget(input_contrasena)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(boton_registrar)
        layout_botones.addWidget(boton_cancelar)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(30)
        layout_principal.addLayout(layout_usuario)
        layout_principal.addSpacing(15)
        layout_principal.addLayout(layout_contrasena)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

        '''Acciones de los botones'''
        boton_cancelar.clicked.connect(self.reject)
        boton_registrar.clicked.connect(self.accept)


class loginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Iniciar sesión")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        '''Título principal'''
        label_1 = QLabel("Iniciar sesión")
        titulo_fuente = QFont()
        titulo_fuente.setPointSize(24)
        titulo_fuente.setBold(True)
        label_1.setFont(titulo_fuente)
        label_1.setAlignment(Qt.AlignCenter)

        '''Etiquetas y campos de entrada'''
        label_2 = QLabel("Usuario:")
        label_3 = QLabel("Contraseña:")

        input_usuario = QLineEdit()
        input_usuario.setFixedHeight(40)
        input_usuario.setMinimumWidth(300)

        input_contrasena = QLineEdit()
        input_contrasena.setEchoMode(QLineEdit.Password)
        input_contrasena.setFixedHeight(40)
        input_contrasena.setMinimumWidth(300)

        '''Botones principales'''
        boton_login = QPushButton("Iniciar sesión")
        boton_login.setFixedSize(150, 40)

        boton_singup = QPushButton("Registrarse")
        boton_singup.setFixedSize(150, 40)

        '''Conexión del botón de registro'''
        boton_singup.clicked.connect(self.abrir_registro)

        '''Organización con layouts'''
        layout_principal = QVBoxLayout()
        layout_secundario = QVBoxLayout()
        layout_secundario_1_1 = QHBoxLayout()
        layout_secundario_2_1 = QHBoxLayout()
        layout_botones = QHBoxLayout()

        layout_principal.addWidget(label_1)
        layout_principal.addSpacing(40)

        layout_secundario_1_1.addWidget(label_2)
        layout_secundario_1_1.addWidget(input_usuario)
        layout_secundario_2_1.addWidget(label_3)
        layout_secundario_2_1.addWidget(input_contrasena)

        layout_botones.addWidget(boton_login)
        layout_botones.addStretch()
        layout_botones.addWidget(boton_singup)

        layout_secundario.addLayout(layout_secundario_1_1)
        layout_secundario.addSpacing(20)
        layout_secundario.addLayout(layout_secundario_2_1)

        layout_principal.addLayout(layout_secundario)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

    def abrir_registro(self):
        '''Abre la ventana de registro'''
        dialogo = RegistroDialog()
        if dialogo.exec_() == QDialog.Accepted:
            print("Usuario registrado con éxito")