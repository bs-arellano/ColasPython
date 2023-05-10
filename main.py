from cpu import Procesador
from gui_factory import GUI_factory

gui_id=3

if __name__=='__main__':
    procesador = Procesador()
    #procesador.agregar_nodo(procesador)
    gui = GUI_factory(id=gui_id, cpu=procesador).gui
    gui.ejecutar()