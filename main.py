import sys
from PyQt5.QtWidgets import QApplication
from windows.login_window import LoginWindow
from windows.main_window import MainWindow
from database.database import *

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv) #Es el objeto principal que inicia y controla la aplicacion grafica
        create_db()  # Crear base de datos si no existe

        #Se instancia la pantalla de login para conectar a ella
        self.login_window = LoginWindow()
        #Cuando login devuelva success (Variable dada a la clase) se enseña el main
        self.login_window.login_success.connect(self.show_main)
        #Se muestra el login al inicio
        self.login_window.show()

    def show_main(self, user_id):
        self.login_window.close()
        self.main_window = MainWindow(user_id)
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = AppController()
    app.run()
