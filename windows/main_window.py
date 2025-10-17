from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox, QFileDialog, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from database.database import get_incidencias, add_incidencia, delete_incidencia, get_titulos_y_estados, update_estado_incidencia, get_datos_para_graficas
from windows.ficheroincidencias import IncidenciaForm


class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Gestor de Incidencias")
        self.resize(950, 500)

        layout = QVBoxLayout()

        # ---------- FILTROS, GRÁFICAS Y EXPORTAR (3 FILAS) ----------
        filtros_container = QWidget()
        filtros_superior = QVBoxLayout()
        filtros_superior.setContentsMargins(20, 20, 20, 10)
        filtros_superior.setSpacing(8)

        # --- Fila 1: filtros ---
        filtros_layout_1 = QHBoxLayout()
        filtros_layout_1.setSpacing(10)

        label_estado = QLabel("Estado:")
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Todos", "pendiente", "cerrado"])
        self.estado_combo.setFixedWidth(110)

        label_prioridad = QLabel("Prioridad:")
        self.prioridad_combo = QComboBox()
        self.prioridad_combo.addItems(["Todos", "baja", "media", "alta", "extrema"])
        self.prioridad_combo.setFixedWidth(110)

        label_desde = QLabel("Desde:")
        self.fecha_desde = QDateEdit()
        self.fecha_desde.setDisplayFormat("yyyy-MM-dd")
        self.fecha_desde.setCalendarPopup(True)
        self.fecha_desde.setDate(QDate.currentDate().addMonths(-1))

        label_hasta = QLabel("Hasta:")
        self.fecha_hasta = QDateEdit()
        self.fecha_hasta.setDisplayFormat("yyyy-MM-dd")
        self.fecha_hasta.setCalendarPopup(True)
        self.fecha_hasta.setDate(QDate.currentDate())

        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_filtrar.setFixedWidth(90)
        self.boton_filtrar.clicked.connect(self.load_data)

        filtros_layout_1.addWidget(label_estado)
        filtros_layout_1.addWidget(self.estado_combo)
        filtros_layout_1.addSpacing(10)
        filtros_layout_1.addWidget(label_prioridad)
        filtros_layout_1.addWidget(self.prioridad_combo)
        filtros_layout_1.addSpacing(10)
        filtros_layout_1.addWidget(label_desde)
        filtros_layout_1.addWidget(self.fecha_desde)
        filtros_layout_1.addWidget(label_hasta)
        filtros_layout_1.addWidget(self.fecha_hasta)
        filtros_layout_1.addSpacing(10)
        filtros_layout_1.addWidget(self.boton_filtrar)
        filtros_layout_1.addStretch()

        # --- Fila 2: gráficas ---
        filtros_layout_2 = QHBoxLayout()
        filtros_layout_2.setSpacing(10)

        label_graficas = QLabel("Gráficas:")

        self.boton_grafica_tipo = QPushButton("Por tipo (categoría)")
        self.boton_grafica_tipo.setFixedWidth(150)
        self.boton_grafica_tipo.clicked.connect(self.mostrar_grafica_por_tipo)

        self.boton_grafica_estado = QPushButton("Por estado")
        self.boton_grafica_estado.setFixedWidth(130)
        self.boton_grafica_estado.clicked.connect(self.mostrar_grafica_por_estado)

        self.boton_grafica_tiempo = QPushButton("Por tiempo de resolución")
        self.boton_grafica_tiempo.setFixedWidth(180)
        self.boton_grafica_tiempo.clicked.connect(self.mostrar_grafica_por_tiempo)

        filtros_layout_2.addWidget(label_graficas)
        filtros_layout_2.addWidget(self.boton_grafica_tipo)
        filtros_layout_2.addWidget(self.boton_grafica_estado)
        filtros_layout_2.addWidget(self.boton_grafica_tiempo)
        filtros_layout_2.addStretch()

        # --- Fila 3: exportar ---
        filtros_layout_3 = QHBoxLayout()
        filtros_layout_3.setSpacing(10)

        label_exportar = QLabel("Exportar:")

        self.boton_exportar_pdf = QPushButton("Exportar a PDF")
        self.boton_exportar_pdf.setFixedWidth(130)
        self.boton_exportar_pdf.clicked.connect(self.exportar_pdf)

        self.boton_exportar_csv = QPushButton("Exportar a CSV")
        self.boton_exportar_csv.setFixedWidth(130)
        self.boton_exportar_csv.clicked.connect(self.exportar_csv)

        filtros_layout_3.addWidget(label_exportar)
        filtros_layout_3.addWidget(self.boton_exportar_pdf)
        filtros_layout_3.addWidget(self.boton_exportar_csv)
        filtros_layout_3.addStretch()

        # --- Combinar las tres filas ---
        filtros_superior.addLayout(filtros_layout_1)
        filtros_superior.addLayout(filtros_layout_2)
        filtros_superior.addLayout(filtros_layout_3)

        filtros_container.setLayout(filtros_superior)
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
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")

        incidencias = get_incidencias(estado, prioridad, fecha_desde, fecha_hasta)
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

    def mostrar_grafica_por_tipo(self):
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")
        datos = get_datos_para_graficas(fecha_desde, fecha_hasta)

        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return

        categorias = [fila[0] for fila in datos if fila[0]]
        conteo = Counter(categorias)

        plt.figure(figsize=(7, 4))
        plt.bar(conteo.keys(), conteo.values())
        plt.title("Incidencias por tipo (categoría)")
        plt.xlabel("Categoría")
        plt.ylabel("Cantidad")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


    def mostrar_grafica_por_estado(self):
        """Gráfico circular: distribución de incidencias por estado."""
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")
        datos = get_datos_para_graficas(fecha_desde, fecha_hasta)

        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return

        estados = [fila[1] for fila in datos if fila[1]]
        conteo_estados = Counter(estados)

        etiquetas, valores = zip(*conteo_estados.items())
        colores = plt.get_cmap('Set3').colors
        plt.figure(figsize=(6, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
        plt.title("Distribución de incidencias por estado")
        plt.axis("equal")
        plt.show()


    def mostrar_grafica_por_tiempo(self):
        """Gráfico de líneas: promedio de tiempo de resolución por categoría."""
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")
        datos = get_datos_para_graficas(fecha_desde, fecha_hasta)

        if not datos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias para mostrar.")
            return

        tiempos = defaultdict(list)

        for categoria, _, fecha_creacion, fecha_resolucion in datos:
            if fecha_resolucion:
                try:
                    f1 = datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    f1 = datetime.strptime(fecha_creacion, "%Y-%m-%d")
                try:
                    f2 = datetime.strptime(fecha_resolucion, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    f2 = datetime.strptime(fecha_resolucion, "%Y-%m-%d")
                dias = (f2 - f1).days
                tiempos[categoria].append(dias)

        if not tiempos:
            QMessageBox.information(self, "Sin datos", "No hay incidencias cerradas con fecha de resolución.")
            return

        categorias = list(tiempos.keys())
        promedios = [sum(v) / len(v) for v in tiempos.values()]

        plt.figure(figsize=(7, 4))
        plt.plot(categorias, promedios, marker='o')
        plt.title("Tiempo promedio de resolución por categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Días promedio")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    # ---------------- EXPORTAR A PDF ---------------- #

    def exportar_pdf(self):
        """Genera un PDF con las incidencias mostradas actualmente en la tabla."""
        estado = self.estado_combo.currentText()
        prioridad = self.prioridad_combo.currentText()
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")

        incidencias = get_incidencias(estado, prioridad, fecha_desde, fecha_hasta)

        if not incidencias:
            QMessageBox.warning(self, "Sin datos", "No hay incidencias para exportar.")
            return

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
        y -= 15
        c.drawString(50, y, f"Rango de fechas: {fecha_desde} a {fecha_hasta}")
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

    def exportar_csv(self):
        import csv

        estado = self.estado_combo.currentText()
        prioridad = self.prioridad_combo.currentText()
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().toString("yyyy-MM-dd")

        incidencias = get_incidencias(estado, prioridad, fecha_desde, fecha_hasta)

        if not incidencias:
            QMessageBox.warning(self, "Sin datos", "No hay incidencias para exportar.")
            return

        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "incidencias.csv", "Archivos CSV (*.csv)")
        if not ruta:
            return

        try:
            with open(ruta, "w", newline="", encoding="utf-8") as archivo_csv:
                escritor = csv.writer(archivo_csv)
                # Cabecera
                escritor.writerow(["ID", "Título", "Descripción", "Categoría", "Estado", "Prioridad", "Fecha creación"])
                # Filas
                for inc in incidencias:
                    escritor.writerow(inc)

            QMessageBox.information(self, "Exportación completa", f"CSV guardado en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el CSV:\n{str(e)}")
