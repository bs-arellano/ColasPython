import gui_1
import gui_2
import gui_3

class GUI_factory:
    gui = None
    def __init__(self, id, cpu):
        if id==1:
            self.gui = gui_1.GUI(cpu)
        elif id==2:
            self.gui= gui_2.GUI(cpu)
        elif id==3:
            self.gui=gui_3.GUI(cpu)