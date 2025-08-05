# 🧮 AhorroPRO - Método 50/30/20

**AhorroPRO** es una aplicación de escritorio desarrollada en Python para ayudarte a gestionar tus finanzas personales utilizando el reconocido método de ahorro **50/30/20**.

Diseñada con una interfaz amigable, moderna y funcional, permite registrar ingresos, gastos clasificados por tipo, calcular tu ahorro ideal y real, visualizar alertas de déficit, exportar reportes en PDF y Excel, y analizar tu rendimiento financiero de forma clara.

---

## 📦 Características principales

- Registro mensual de:
  - Ingreso total
  - Gastos clasificados (Necesidades / Ocio / Categorías)
  - Ahorro manual u automático
- Cálculo automático de ideales (50/30/20)
- Tabla resumen anual de 12 meses
- Ventana interactiva de ingreso de datos
- Validaciones y alertas de ahorro en déficit
- Exportación profesional a **PDF** (con logo, KPIs, gráficos, resumen)
- Exportación a **Excel** con dashboard
- Gráficos comparativos integrados (Tkinter + PDF)

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
https://github.com/tuusuario/ahorropro.git
cd ahorropro
```

### 2. Crea el entorno virtual e instala dependencias

```bash
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Ejecuta la aplicación

```bash
python main.py
```

---

## 🛠 Requisitos

- Python 3.10 o superior
- Paquetes: `ttkbootstrap`, `matplotlib`, `pandas`, `reportlab`

Puedes instalarlos con:

```bash
pip install -r requirements.txt
```

---

## 📄 Compilación a .EXE (opcional)

Si deseas crear un ejecutable:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=assets/logo.ico main.py
```

El archivo resultante estará en la carpeta `dist/`.

---

## 📂 Estructura del proyecto

```
AhorroPRO/
├── assets/             # Imágenes, logo
├── reportes/           # PDFs generados
├── main.py
├── vista.py
├── modelo.py
├── controlador.py
├── requirements.txt
└── README.md
```

---

## 📌 Créditos

Desarrollado por Charletsts.\
Inspirado en el método financiero 50/30/20 de Elizabeth Warren.

---

## 📘 Licencia

Este proyecto es de uso personal y educativo. Puedes modificarlo libremente para tus propias finanzas. No se recomienda usarlo como sistema contable empresarial sin adaptaciones adicionales.

---

## 🌟 Futuras mejoras

- Panel de ajustes con configuración personalizada (porcentaje ahorro, umbral)
- Resumen acumulado anual con gráficos
- Exportación a CSV/JSON
- Clonar datos de meses anteriores
- Modo multiusuario (opcional)

