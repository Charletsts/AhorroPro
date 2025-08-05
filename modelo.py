# modelo.py
"""
Modelo de datos para AhorroPRO
Estructura principal: DataFrame mensual y detalle de gastos
"""

import pandas as pd
import os

class ModeloAhorro:
    def __init__(self):
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.registro_mensual = pd.DataFrame({
            "Mes": self.meses,
            "Ingresos Reales": [0.0] * 12,
            "Gastos Necesidades": [0.0] * 12,
            "Gastos Ocio": [0.0] * 12,
            "Ahorro Real": [0.0] * 12,
            "Ahorro Ideal": [0.0] * 12,
            "Estado": ["" for _ in self.meses]
        })

        self.gastos_detalle = pd.DataFrame(columns=["Mes", "Descripción", "Monto", "Tipo", "Categoría"])

    def agregar_gasto(self, mes, descripcion, monto, tipo, categoria):
        """Agrega un gasto al detalle y actualiza resumen mensual"""
        nuevo = {
            "Mes": mes,
            "Descripción": descripcion,
            "Monto": monto,
            "Tipo": tipo,
            "Categoría": categoria
        }
        self.gastos_detalle = pd.concat([self.gastos_detalle, pd.DataFrame([nuevo])], ignore_index=True)

        idx = self.registro_mensual.index[self.registro_mensual["Mes"] == mes][0]
        if tipo == "Necesidad":
            self.registro_mensual.at[idx, "Gastos Necesidades"] += monto
        elif tipo == "Ocio":
            self.registro_mensual.at[idx, "Gastos Ocio"] += monto

        # Recalcular ahorro real
        ingresos = self.registro_mensual.at[idx, "Ingresos Reales"]
        gastos = self.registro_mensual.at[idx, "Gastos Necesidades"] + self.registro_mensual.at[idx, "Gastos Ocio"]
        ahorro = ingresos - gastos
        self.registro_mensual.at[idx, "Ahorro Real"] = ahorro
        self.registro_mensual.at[idx, "Ahorro Ideal"] = ingresos * 0.2
        self.registro_mensual.at[idx, "Estado"] = "✅ Correcto" if ahorro >= ingresos * 0.2 else "⚠ Déficit"

    def guardar_registro(self, data):
        df = pd.DataFrame(data)
        with pd.ExcelWriter("registro_finanzas.xlsx") as writer:
            df.to_excel(writer, sheet_name="Resumen", index=False)
            self.gastos_detalle.to_excel(writer, sheet_name="Gastos Detalle", index=False)
        self.registro_mensual = df

    def cargar_registro(self, anio):
        if os.path.exists("registro_finanzas.xlsx"):
            df = pd.read_excel("registro_finanzas.xlsx", sheet_name="Resumen")
            gastos = pd.read_excel("registro_finanzas.xlsx", sheet_name="Gastos Detalle")
            self.registro_mensual = df
            self.gastos_detalle = gastos
        return self.registro_mensual
