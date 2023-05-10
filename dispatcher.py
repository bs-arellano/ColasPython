from nodo import Proceso
class Dispatcher:
    def __init__(self):
        self.listos = []
        self.bloqueados = []
    
    def agregar(self, proceso: Proceso):
        self.listos.append(proceso)
    
    def get(self) -> Proceso:
        self.listos.sort(key=lambda x: x.prioridad)
        return self.listos.pop()
    def peek(self) -> Proceso:
        self.listos.sort(key=lambda x: x.t_llegada)
        return self.listos[-1]
    def size(self):
        return len(self.listos)