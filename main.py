import sys

from PyQt5.QtWidgets import QApplication
from main_window import mainWindow

'''
    Definicion de la aplicacion, este archivo manejara la aplicacion
'''

def main():
    app = QApplication(sys.argv)

    app.exec()

if __name__ == "__main__":
    main()
