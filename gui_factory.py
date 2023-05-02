import gui_1
import gui_2

class GUI_factory:
    gui = None
    def __init__(self, id, cpu):
        if id==1:
            self.gui = gui_1.GUI(cpu)
        elif id==2:
            self.gui= gui_2.GUI(cpu)