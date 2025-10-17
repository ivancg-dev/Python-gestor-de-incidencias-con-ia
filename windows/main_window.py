from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from collections import Counter
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from database.database import get_incidencias, add_incidencia, delete_incidencia, get_titulos_y_estados, update_estado_incidencia
from windows.ficheroincidencias import IncidenciaForm


class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestor de Incidencias")
        self.resize(850, 500)

        layout = QVBoxLayout()

        # ---------- FILTROS ----------
        filtros_container = QWidget()
        filtros_layout = QHBoxLayout()
        filtros_layout.setContentsMargins(20, 20, 20, 10)
        filtros_layout.setSpacing(10)

        label_estado = QLabel("Estado:")
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Todos", "pendiente", "cerrado"])
        self.estado_combo.setFixedWidth(110)

        label_prioridad = QLabel("Prioridad:")
        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(["Todos", "baja", "media", "alta", "extrema"])
        self.prioridad_combo.setFixedWidth(110)

        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_filtrar.setFixedWidth(90)
        self.boton_filtrar.clicked.connect(self.load_data)

        self.boton_grafica_circular = QPushButton("Gráfica circular")
        self.boton_grafica_circular.setFixedWidth(130)
        self.boton_grafica_circular.clicked.connect(self.mostrar_grafica_estado_1)

        self.boton_grafica_barras = QPushButton("Gráfica de barras")
        self.boton_grafica_barras.setFixedWidth(130)
        self.boton_grafica_barras.clicked.connect(self.mostrar_grafica_estado_2)

        # NUEVO BOTÓN: Exportar a PDF
        self.boton_exportar_pdf = QPushButton("Exportar a PDF")
        self.boton_exportar_pdf.setFixedWidth(130)
        self.boton_exportar_pdf.clicked.connect(self.exportar_pdf)

        filtros_layout.addWidget(label_estado)
        filtros_layout.addWidget(self.estado_combo)
        filtros_layout.addSpacing(15)
        filtros_layout.addWidget(label_prioridad)
        filtros_layout.addWidget(self.prioridad_combo)
        filtros_layout.addSpacing(10)
        filtros_layout.addWidget(self.boton_filtrar)
        filtros_layout.addStretch()
        filtros_layout.addWidget(self.boton_grafica_circular)
        filtros_layout.addWidget(self.boton_grafica_barras)
        filtros_layout.addWidget(self.boton_exportar_pdf)

        filtros_container.setLayout(filtros_layout)
        layout.addWidget(filtros_container)

        # ---------- TABLA ----------
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título", "Descripción", "Categoría", "Estado", "Prioridad", "Fecha creación"
        ])
        layout.addWidget(self.table)

        # ---------- ACCIONES ----------
        acciones = QHBoxLayout()
        self.btn_add = QPushButton("Agregar")
        self.btn_add.clicked.connect(self.show_incidencias)

        self.btn_toggle_estado = QPushButton("Cambiar estado")
        self.btn_toggle_estado.clicked.connect(self.toggle_estado)

        self.btn_delete = QPushButton("Eliminar seleccionada")
        self.btn_delete.clicked.connect(self.delete_incidencia)

        acciones.addWidget(self.btn_add)
        acciones.addWidget(self.btn_toggle_estado)
        acciones.addWidget(self.btn_delete)

        layout.addLayout(acciones)

        self.setLayout(layout)
        self.load_data()

    # ---------------- FUNCIONES PRINCIPALES ---------------- #

    def load_data(self):
        estado = self.estado_combo.currentText()
        prioridad = self.prioridad_combo.currentText()
        incidencias = get_incidencias(estado, prioridad)
        self.table.setRowCount(len(incidencias))

        for row, inc in enumerate(incidencias):
            for col, valor in enumerate(inc):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def delete_incidencia(self):
        fila = self.table.currentRow()
        if fila >= 0:
            incidencia_id = int(self.table.item(fila, 0).text())
            delete_incidencia(incidencia_id)
            self.load_data()
            QMessageBox.information(self, "Eliminación exitosa", "La incidencia ha sido eliminada correctamente.")
        else:
            QMessageBox.warning(self, "Sin selección", "Selecciona una incidencia para eliminar.")

    def toggle_estado(self):
        fila = self.table.currentRow()
        if fila >= 0:
            incidencia_id = int(self.table.item(fila, 0).text())
            estado_actual = self.table.item(fila, 4).text()
            nuevo_estado = "cerrado" if estado_actual == "pendiente" else "pendiente"
            update_estado_incidencia(incidencia_id, nuevo_estado)
            self.load_data()
            QMessageBox.information(self, "Estado actualizado", f"Estado cambiado a '{nuevo_estado}'.")
        else:
            QMessageBox.warning(self, "Sin selección", "Selecciona una incidencia para cambiar su estado.")

    def show_incidencias(self):
        self.ficheroincidencias = IncidenciaForm(self.user_id)
        self.ficheroincidencias.incidencia_registrada.connect(self.load_data)
        self.ficheroincidencias.show()

    # ---------------- GRÁFICAS ---------------- #

    def mostrar_grafica_estado_1(self):
        datos = get_titulos_y_estados()
        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return
        estados = [estado for _, estado in datos]
        conteo_estados = Counter(estados)
        etiquetas, valores = zip(*sorted(conteo_estados.items(), key=lambda x: x[1], reverse=True))
        colores = plt.get_cmap('Set3').colors
        plt.figure(figsize=(6, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
        plt.title('Distribución de Incidencias por Estado')
        plt.axis('equal')
        plt.show()

    def mostrar_grafica_estado_2(self):
        datos = get_titulos_y_estados()
        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return
        estados = [estado for _, estado in datos]
        conteo_estados = Counter(estados)
        etiquetas, valores = zip(*conteo_estados.items())
        plt.figure(figsize=(6, 4))
        plt.bar(etiquetas, valores)
        plt.title('Número de Incidencias por Estado')
        plt.xlabel('Estado')
        plt.ylabel('Cantidad')
        plt.show()

    # ---------------- EXPORTAR A PDF ---------------- #

    def exportar_pdf(self):
        """Genera un PDF con las incidencias mostradas actualmente en la tabla."""
        estado = self.estado_combo.currentText()
        prioridad = self.prioridad_combo.currentText()
        incidencias = get_incidencias(estado, prioridad)

        if not incidencias:
            QMessageBox.warning(self, "Sin datos", "No hay incidencias para exportar.")
            return

        # Pedir al usuario dónde guardar el PDF
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "incidencias.pdf", "Archivos PDF (*.pdf)")
        if not ruta:
            return

        c = canvas.Canvas(ruta, pagesize=A4)
        ancho, alto = A4
        y = alto - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Informe de Incidencias")
        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Estado: {estado} | Prioridad: {prioridad}")
        y -= 30

        for inc in incidencias:
            if y < 80:
                c.showPage()
                y = alto - 50
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, f"ID: {inc[0]}  |  {inc[1]}")
            y -= 15
            c.setFont("Helvetica", 9)
            c.drawString(60, y, f"Descripción: {inc[2]}")
            y -= 12
            c.drawString(60, y, f"Categoría: {inc[3]} | Estado: {inc[4]} | Prioridad: {inc[5]} | Fecha: {inc[6]}")
            y -= 25

        c.save()
        QMessageBox.information(self, "Exportación completa", f"PDF guardado en:\n{ruta}")
