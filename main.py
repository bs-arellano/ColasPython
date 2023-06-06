from procesador import Procesador
from gui import GUI
from test import Test

dev = False

cpu=Procesador()
if dev:
    Test(cpu)
else:
    gui=GUI(cpu)
    gui.ejecutar()