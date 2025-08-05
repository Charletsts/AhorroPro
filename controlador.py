# controlador.py
"""
Controlador principal de AhorroPRO - Versión PRO
Incluye:
- Ventana “Ingreso Gastos” rediseñada
- Registro de ingresos, gastos y ahorro
- Validaciones y actualización dinámica de tablas
- Exportación PDF profesional con KPIs y gráficos
- Gráficos comparativos embebidos en ventana y PDF
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import ttkbootstrap as tb
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ControladorAhorro:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def cargar_anio(self):
        anio = self.vista.anio_var.get()
        if not anio.isdigit():
            messagebox.showerror("Error", "Año inválido.")
            return
        data = self.modelo.cargar_registro(anio)
        self.vista.actualizar_tabla(data)
        self.vista.actualizar_gastos_detallados(self.modelo.gastos_detalle)
        self.vista.mostrar_mensaje(f"Año {anio} cargado correctamente.")

    def guardar_cambios(self):
        datos = []
        for iid in self.vista.tree.get_children():
            vals = self.vista.tree.item(iid)['values']
            datos.append({
                "Mes": vals[0], "Ingresos Reales": float(vals[1]),
                "Gastos Necesidades": float(vals[2]), "Gastos Ocio": float(vals[3]),
                "Ahorro Real": float(vals[4]), "Ahorro Ideal": float(vals[5]), "Estado": vals[6]
            })
        self.modelo.guardar_registro(datos)
        messagebox.showinfo("Guardado", "Datos actualizados correctamente.")
        self.vista.mostrar_mensaje("Cambios guardados en archivo Excel.")

    def mostrar_ventana_ingreso_gastos(self):
        ventana = tb.Toplevel(title="Ingreso de Datos Financieros")
        ventana.geometry("700x600")
        ventana.resizable(True, True)

        # Variables
        ingreso_var = tb.StringVar()
        descripcion_var = tb.StringVar()
        monto_var = tb.StringVar()
        tipo_var = tb.StringVar(value="Necesidad")
        categoria_var = tb.StringVar()
        ahorro_manual_var = tb.StringVar()
        mes_var = tb.StringVar(value="Enero")
        lista_categorias = ["Transporte", "Hogar", "Alimentación", "Salud", "Educación"]

        # Contenedor con scroll
        canvas_frame = tb.Frame(ventana)
        canvas_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(canvas_frame)
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = tb.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        scrollable_frame = tb.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # --- Ingreso del Mes ---
        lf_ingreso = tb.LabelFrame(scrollable_frame, text="📥 Ingreso Mensual")
        lf_ingreso.pack(fill='x', pady=10)

        tb.Label(lf_ingreso, text="Ingreso del Mes:").pack(anchor='w')
        entry_ingreso = tb.Entry(lf_ingreso, textvariable=ingreso_var)
        entry_ingreso.pack(fill='x')

        label_ideales = tb.Label(lf_ingreso, text="💡 Ideales → Necesidades: $0 | Ocio: $0 | Ahorro: $0", foreground="purple")
        label_ideales.pack(pady=5)

        def actualizar_ideales(event=None):
            try:
                valor = ingreso_var.get()
                if valor.strip() == "":
                    return
                ingreso = float(valor)
                label_ideales.config(
                    text=f"💡 Ideales → Necesidades: ${ingreso * 0.5:,.0f} | Ocio: ${ingreso * 0.3:,.0f} | Ahorro: ${ingreso * 0.2:,.0f}"
                )
            except:
                pass

        entry_ingreso.bind("<KeyRelease>", actualizar_ideales)
        ingreso_var.trace_add("write", actualizar_ideales)

        # --- Registrar Gasto ---
        lf_gasto = tb.LabelFrame(scrollable_frame, text="📝 Registrar Gasto")
        lf_gasto.pack(fill='x', pady=10)

        tb.Label(lf_gasto, text="Descripción:").pack(anchor='w')
        tb.Entry(lf_gasto, textvariable=descripcion_var).pack(fill='x')

        tb.Label(lf_gasto, text="Monto:").pack(anchor='w')
        tb.Entry(lf_gasto, textvariable=monto_var).pack(fill='x')

        tb.Label(lf_gasto, text="Tipo:").pack(anchor='w')
        tipo_frame = tb.Frame(lf_gasto)
        tipo_frame.pack(anchor='w', pady=2)
        tb.Radiobutton(tipo_frame, text="Necesidad", variable=tipo_var, value="Necesidad").pack(side='left', padx=10)
        tb.Radiobutton(tipo_frame, text="Ocio", variable=tipo_var, value="Ocio").pack(side='left')

        tb.Label(lf_gasto, text="Categoría:").pack(anchor='w')
        cat_frame = tb.Frame(lf_gasto)
        cat_frame.pack(fill='x')
        cb_categoria = tb.Combobox(cat_frame, textvariable=categoria_var, values=lista_categorias, width=30)
        cb_categoria.pack(side='left', padx=5, fill='x', expand=True)

        def agregar_categoria():
            nueva = simpledialog.askstring("Nueva Categoría", "Nombre de la categoría:")
            if nueva and nueva not in lista_categorias:
                lista_categorias.append(nueva)
                cb_categoria.config(values=lista_categorias)
                categoria_var.set(nueva)

        tb.Button(cat_frame, text="➕ Agregar Categoría", bootstyle="secondary", command=agregar_categoria).pack(side='left', padx=5)

        tb.Label(lf_gasto, text="Mes:").pack(anchor='w')
        cb_mes = tb.Combobox(lf_gasto, textvariable=mes_var, values=self.modelo.meses, width=25)
        cb_mes.pack(fill='x')

        # --- Tabla de gastos temporales ---
        tabla_temp = tb.Treeview(scrollable_frame, columns=("desc", "monto", "tipo", "categoria"), show="headings", height=5)
        for col in ("desc", "monto", "tipo", "categoria"):
            tabla_temp.heading(col, text=col.capitalize())
            tabla_temp.column(col, width=150)
        tabla_temp.pack(fill='x', pady=10)

        gastos_temp = []

        def agregar_gasto_temp():
            try:
                monto = float(monto_var.get())
                desc = descripcion_var.get().strip()
                if not desc:
                    raise ValueError("Falta descripción.")
                tipo = tipo_var.get()
                cat = categoria_var.get()
                tabla_temp.insert("", "end", values=(desc, monto, tipo, cat))
                gastos_temp.append((desc, monto, tipo, cat))
                descripcion_var.set("")
                monto_var.set("")
            except:
                messagebox.showerror("Error", "Verifica descripción y monto válido.")

        tb.Button(scrollable_frame, text="✅ Agregar Gasto", bootstyle="success", command=agregar_gasto_temp).pack(pady=5)

        # --- Ahorro Manual ---
        lf_ahorro = tb.LabelFrame(scrollable_frame, text="💰 Ahorro Manual (opcional)")
        lf_ahorro.pack(fill='x', pady=10)
        tb.Entry(lf_ahorro, textvariable=ahorro_manual_var).pack(fill='x', padx=5, pady=5)

        # --- Guardar Todo ---
        def guardar_todo():
            mes = mes_var.get()
            try:
                if ingreso_var.get():
                    ingreso = float(ingreso_var.get())
                    idx = self.modelo.registro_mensual.index[self.modelo.registro_mensual["Mes"] == mes][0]
                    self.modelo.registro_mensual.at[idx, "Ingresos Reales"] = ingreso
                    self.modelo.registro_mensual.at[idx, "Ahorro Ideal"] = ingreso * 0.2
            except:
                pass

            for desc, monto, tipo, cat in gastos_temp:
                self.modelo.agregar_gasto(mes, desc, monto, tipo, cat)

            if ahorro_manual_var.get():
                try:
                    ahorro = float(ahorro_manual_var.get())
                    idx = self.modelo.registro_mensual.index[self.modelo.registro_mensual["Mes"] == mes][0]
                    self.modelo.registro_mensual.at[idx, "Ahorro Real"] += ahorro
                except:
                    pass

            self.vista.actualizar_tabla(self.modelo.registro_mensual)
            self.vista.actualizar_gastos_detallados(self.modelo.gastos_detalle)
            ventana.destroy()

        tb.Button(scrollable_frame, text="💾 Guardar Todo", bootstyle="primary", command=guardar_todo).pack(pady=10)

    def mostrar_graficos(self):
        import tkinter as tk
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        df = self.modelo.registro_mensual
        meses = df["Mes"]
        ahorro_real = df["Ahorro Real"]
        ahorro_ideal = df["Ahorro Ideal"]
        gastos_necesidades = df["Gastos Necesidades"]
        gastos_ocio = df["Gastos Ocio"]

        ventana = tk.Toplevel()
        ventana.title("Gráficos Comparativos")
        ventana.geometry("1000x800")

        fig, axs = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True)
        fig.suptitle("Análisis Comparativo Real vs Ideal", fontsize=14)

        axs[0].bar(meses, ahorro_real, label="Ahorro Real", color="#4CAF50")
        axs[0].plot(meses, ahorro_ideal, label="Ahorro Ideal", color="#FF5722", marker="o", linestyle="--")
        axs[0].set_title("Ahorro Real vs Ahorro Ideal")
        axs[0].legend()
        axs[0].set_ylabel("$ CLP")

        axs[1].bar(meses, gastos_necesidades, label="Necesidades", color="#2196F3")
        axs[1].bar(meses, gastos_ocio, label="Ocio", bottom=gastos_necesidades, color="#FFC107")
        axs[1].set_title("Distribución de Gastos (Necesidades + Ocio)")
        axs[1].legend()
        axs[1].set_ylabel("$ CLP")

        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def exportar_pdf(self):
        os.makedirs("reportes", exist_ok=True)
        año = self.vista.anio_var.get()
        filename = f"reportes/Reporte_AhorroPRO_{año}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        estilo_titulo = styles['Title']
        estilo_normal = styles['Normal']
        estilo_h2 = styles['Heading2']

        try:
            logo_path = os.path.join("assets", "logo.png")
            img = RLImage(logo_path, width=120, height=60)
            img.hAlign = 'CENTER'
            story.append(img)
        except Exception:
            story.append(Paragraph("AhorroPRO", estilo_titulo))

        story.append(Spacer(1, 12))
        story.append(Paragraph("Reporte Financiero 50/30/20", estilo_titulo))
        story.append(Paragraph(f"Año: {año}", estilo_normal))
        story.append(Paragraph(f"Fecha de generación: {datetime.date.today()}", estilo_normal))
        story.append(Spacer(1, 20))

        df = self.modelo.registro_mensual
        ingreso_total = df["Ingresos Reales"].sum()
        ingreso_prom = df["Ingresos Reales"].mean()
        ahorro_total = df["Ahorro Real"].sum()
        ahorro_prom = df["Ahorro Real"].mean()
        ahorro_ideal_total = df["Ahorro Ideal"].sum()
        estado_global = "✅ Correcto" if ahorro_total >= ahorro_ideal_total else "⚠ Déficit"

        story.append(Paragraph("📊 KPIs del Año", estilo_h2))
        story.append(Paragraph(f"Ingreso Total: ${ingreso_total:,.0f}", estilo_normal))
        story.append(Paragraph(f"Ahorro Total: ${ahorro_total:,.0f}", estilo_normal))
        story.append(Paragraph(f"Ahorro Ideal: ${ahorro_ideal_total:,.0f}", estilo_normal))
        story.append(Paragraph(f"Estado Global: {estado_global}", estilo_normal))
        story.append(Spacer(1, 20))

        story.append(Paragraph("📅 Resumen Mensual", estilo_h2))
        resumen_data = [["Mes", "Ingresos", "Necesidades", "Ocio", "Ahorro", "Ideal", "Estado"]]
        for _, row in df.iterrows():
            resumen_data.append([
                row["Mes"],
                f"${row['Ingresos Reales']:,.0f}",
                f"${row['Gastos Necesidades']:,.0f}",
                f"${row['Gastos Ocio']:,.0f}",
                f"${row['Ahorro Real']:,.0f}",
                f"${row['Ahorro Ideal']:,.0f}",
                row["Estado"]
            ])

        tabla = Table(resumen_data, repeatRows=1, hAlign='LEFT')
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
        ]))
        story.append(tabla)

        try:
            # Gráficos
            fig1, ax1 = plt.subplots(figsize=(6, 3))
            ax1.bar(df["Mes"], df["Ahorro Real"], label="Ahorro Real", color="#4CAF50")
            ax1.plot(df["Mes"], df["Ahorro Ideal"], label="Ahorro Ideal", color="#FF5722", linestyle="--", marker="o")
            ax1.set_title("Ahorro Real vs Ideal")
            ax1.legend()
            ahorro_img = "reportes/ahorro_temp.png"
            fig1.savefig(ahorro_img, bbox_inches='tight')
            plt.close(fig1)
            story.append(Spacer(1, 12))
            story.append(RLImage(ahorro_img, width=450, height=250))

            fig2, ax2 = plt.subplots(figsize=(6, 3))
            ax2.bar(df["Mes"], df["Gastos Necesidades"], label="Necesidades", color="#2196F3")
            ax2.bar(df["Mes"], df["Gastos Ocio"], label="Ocio", bottom=df["Gastos Necesidades"], color="#FFC107")
            ax2.set_title("Gastos Mensuales")
            ax2.legend()
            gastos_img = "reportes/gastos_temp.png"
            fig2.savefig(gastos_img, bbox_inches='tight')
            plt.close(fig2)
            story.append(Spacer(1, 12))
            story.append(RLImage(gastos_img, width=450, height=250))

        except Exception as e:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Error al generar gráficos: " + str(e), estilo_normal))

        try:
            doc.build(story)
            messagebox.showinfo("Éxito", f"Reporte exportado como PDF:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el PDF:\n{e}")
