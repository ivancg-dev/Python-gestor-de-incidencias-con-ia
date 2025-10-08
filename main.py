import sys

from PyQt5.QtWidgets import QApplication
from login_window import loginWindow
from main_window import mainWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        #Crear ventanas
        self.login_window = loginWindow()
        self.main_window = None
        #Conectar señales
        self.login_window.login_successful.connect(self.show_main_window)
        #Mostrar ventana de login
        self.login_window.show()

    def show_main_window(self, username):
        self.main_window = mainWindow(username)
        self.login_window.close()
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
