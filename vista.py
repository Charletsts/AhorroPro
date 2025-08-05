# vista.py
"""
Vista principal de AhorroPRO (Versión PRO)
Interfaz moderna con ttkbootstrap:
- Tabla principal (resumen mensual)
- Tabla de gastos detallados
- Botonera con acciones clave
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox

class VistaAhorro:
    def __init__(self):
        self.controlador = None
        self.root = tb.Window(themename="cosmo")  # Tema visual moderno
        self.root.title("Ahorro 50/30/20 - Versión PRO")
        self.root.geometry("1300x850")
        self.root.resizable(True, True)

        # Variables
        self.anio_var = tb.StringVar(value='2025')
        self.status_var = tb.StringVar(value="")
        self.umbral_var = tb.DoubleVar(value=10.0)
        self.porcentaje_ahorro_var = tb.DoubleVar(value=20.0)

        # UI
        self.crear_widgets()

    def crear_widgets(self):
        frame_top = tb.Frame(self.root)
        frame_top.pack(fill=X, pady=10)

        tb.Label(frame_top, text="Año:").pack(side=LEFT, padx=5)
        tb.Entry(frame_top, textvariable=self.anio_var, width=10).pack(side=LEFT)

        tb.Label(frame_top, text="Alerta Ahorro (%)").pack(side=LEFT, padx=5)
        tb.Spinbox(frame_top, from_=5, to=50, width=5, textvariable=self.umbral_var).pack(side=LEFT, padx=5)

        self.boton_frame = tb.Frame(frame_top)
        self.boton_frame.pack(side=RIGHT)

        # Tabla resumen mensual
        tb.Label(self.root, text="📊 Registro Mensual", bootstyle="primary", font=("Arial", 14, "bold")).pack()
        cols = ("Mes", "Ingresos", "Necesidades", "Ocio", "Ahorro", "Ideal", "Estado")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(padx=10, pady=10, fill=X)

        # Tabla de gastos detallados
        tb.Label(self.root, text="🧾 Gastos Detallados", bootstyle="secondary", font=("Arial", 14, "bold")).pack()
        cols_g = ("Mes", "Descripción", "Monto", "Tipo", "Categoría")
        self.tree_gastos = ttk.Treeview(self.root, columns=cols_g, show="headings", height=8)
        for col in cols_g:
            self.tree_gastos.heading(col, text=col)
            self.tree_gastos.column(col, width=160)
        self.tree_gastos.pack(padx=10, pady=10, fill=X)

        # Estado inferior
        tb.Label(self.root, textvariable=self.status_var, anchor='w').pack(fill=X, padx=10, pady=5)

    def configurar_botones(self):
        tb.Button(self.boton_frame, text="📂 Cargar Año", bootstyle="info", command=self.controlador.cargar_anio).pack(side=LEFT, padx=5)
        tb.Button(self.boton_frame, text="💾 Guardar", bootstyle="success", command=self.controlador.guardar_cambios).pack(side=LEFT, padx=5)
        tb.Button(self.boton_frame, text="📥 Ingreso Gastos", bootstyle="primary", command=self.controlador.mostrar_ventana_ingreso_gastos).pack(side=LEFT, padx=5)
        tb.Button(self.boton_frame, text="📊 Gráficos", bootstyle="warning", command=self.controlador.mostrar_graficos).pack(side=LEFT, padx=5)
        tb.Button(self.boton_frame, text="📄 Exportar PDF", bootstyle="secondary", command=self.controlador.exportar_pdf).pack(side=LEFT, padx=5)

    def actualizar_tabla(self, data):
        """Refresca la tabla principal de resumen mensual"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=(
                row["Mes"], row["Ingresos Reales"], row["Gastos Necesidades"],
                row["Gastos Ocio"], row["Ahorro Real"], row["Ahorro Ideal"], row["Estado"]
            ))

    def actualizar_gastos_detallados(self, gastos):
        """Refresca la tabla de gastos detallados"""
        for i in self.tree_gastos.get_children():
            self.tree_gastos.delete(i)
        for _, row in gastos.iterrows():
            self.tree_gastos.insert("", "end", values=(
                row["Mes"], row["Descripción"], row["Monto"], row["Tipo"], row["Categoría"]
            ))

    def mostrar_mensaje(self, texto):
        """Actualiza el estado inferior"""
        self.status_var.set(texto)

    def iniciar(self):
        self.root.mainloop()
