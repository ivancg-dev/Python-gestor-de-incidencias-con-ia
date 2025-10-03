import sys

from PyQt5.QtWidgets import QApplication
from windows.main_window import mainWindow

'''
    Definicion de la aplicacion, este archivo manejara la aplicacion
'''

def main():
    app = QApplication(sys.argv)

    main_window = mainWindow()

    main_window.show()

    sys.exit(app.exec_() )

if __name__ == "__main__":
    main()

