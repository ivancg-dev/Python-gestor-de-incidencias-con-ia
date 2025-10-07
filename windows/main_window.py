from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Incidencias con IA")
        self.setFixedSize(800,400)

        layout_principal = QVBoxLayout()
        layout_filtros = QHBoxLayout()
        layout_bloque_incidencias = QHBoxLayout()
        layout_botones_incidencias = QVBoxLayout()

        input_filtro = QLineEdit(self)
        layout_filtros.addWidget(input_filtro)

        layout_principal.addLayout(layout_filtros)
        layout_principal.addLayout(layout_bloque_incidencias)



        '''hola'''


        self.setLayout = layout_principal
    

