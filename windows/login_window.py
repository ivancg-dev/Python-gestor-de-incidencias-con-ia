from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from database.database import *

class LoginWindow(QWidget):
    login_success = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (solo para registro)")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login_user)

        self.register_button = QPushButton("Registrar nuevo usuario")
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel("Inicia sesión o regístrate"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login_user(self):
        usuario = self.user_input.text()
        password = self.pass_input.text()

        user_id = verificar_usuario(usuario, password)
        if user_id:
            self.login_success.emit(user_id)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def register_user(self):
        usuario = self.user_input.text()
        email = self.email_input.text()
        password = self.pass_input.text()

        if usuario and email and password:
            crear_usuario(usuario, email, password)
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
        else:
            QMessageBox.warning(self, "Error", "Completa todos los campos")