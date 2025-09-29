import sys

from PyQt5.QtWidgets import QApplication, QWidget

from windows.main_window import MainWindow

'''
    Definicion de la aplicacion, este archivo manejara la aplicacion
'''

def main():
    app = QApplication(sys.argv)

    main_window = QWidget()
    main_window.show()

    app.exec()

if __name__ == "__main__":
    main()
