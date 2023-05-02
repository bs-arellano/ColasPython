from procesador import Procesador
from gui_factory import GUI_factory

gui_id=1

if __name__=='__main__':
    procesador = Procesador(5)
    procesador.agregar_nodo(procesador)
    gui = GUI_factory(id=gui_id, cpu=procesador).gui
    gui.ejecutar()