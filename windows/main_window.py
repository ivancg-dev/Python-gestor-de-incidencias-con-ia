from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QGridLayout, QSizePolicy
)



class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación PyQt5")
        self.setMinimumSize(900, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout(central_widget)

        # --- Parte superior: buscador y dos botones ---
        top_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar...")
        btn1 = QPushButton("Botón 1")
        btn2 = QPushButton("Botón 2")

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(btn1)
        top_layout.addWidget(btn2)

        # --- Parte inferior: tabla (70%) + botones (30%) ---
        bottom_layout = QHBoxLayout()

        # Tabla
        self.table = QTableWidget(10, 3)  # ejemplo: 10 filas, 3 columnas
        self.table.setHorizontalHeaderLabels(["Columna 1", "Columna 2", "Columna 3"])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Relleno inicial de ejemplo
        for i in range(10):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i+1}-{j+1}"))

        # Botones de la derecha
        right_buttons_layout = QVBoxLayout()
        '''
        right_buttons_layout.setAlignment(Qt.AlignTop)
        '''
        btn_names = ["Acción 1", "Acción 2", "Acción 3", "Acción 4"]
        self.action_buttons = []

        for name in btn_names:
            btn = QPushButton(name)
            btn.setMinimumHeight(40)
            right_buttons_layout.addWidget(btn)
            self.action_buttons.append(btn)

        # Añadir la tabla y la columna de botones al layout inferior
        bottom_layout.addWidget(self.table, 7)   # 70%
        bottom_layout.addLayout(right_buttons_layout, 3)  # 30%

        # Agregar los layouts al layout principal
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
