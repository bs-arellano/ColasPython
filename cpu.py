from dispatcher import Dispatcher
from nodo import Proceso
class Procesador:
    def __init__(self):
        self.estado = 0
        self.dispatcher = Dispatcher()
    def agregar_proceso(self, proceso: Proceso):
        self.dispatcher.agregar(proceso)
    def atender(self):
        proceso: Proceso = self.dispatcher.get()
        if proceso is not None:
            self.estado=1
            proceso.transacciones=0
            self.estado=0