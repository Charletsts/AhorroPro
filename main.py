# main.py
from modelo import ModeloAhorro
from vista import VistaAhorro
from controlador import ControladorAhorro

if __name__ == "__main__":
    modelo = ModeloAhorro()
    vista = VistaAhorro()
    controlador = ControladorAhorro(modelo, vista)
    vista.controlador = controlador
    vista.configurar_botones()
    vista.iniciar()
