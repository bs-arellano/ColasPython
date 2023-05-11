from proceso import Proceso
from dispatcher import Dispatcher

class Procesador:
    def __init__(self):
       self.dispatcher = Dispatcher()
       self.cola:Proceso=None
    def agregar_proceso(self, p: Proceso):
        self.dispatcher.add(p)
    def atender(self, tiempo):
        if self.cola is not None:
            #print(f"[{tiempo}] el proceso actual sale en {self.cola.final}")
            if tiempo==self.cola.final:
                self.cola.final=tiempo
                self.cola.retorno=self.cola.final-self.cola.llegada[0]
                self.cola.espera=self.cola.retorno-self.cola.rafaga[0]
                self.dispatcher.terminados.append(self.cola)
            elif tiempo==self.cola.comienzo[0]+self.cola.bloqueo[0]:
                self.cola.llegada.append(tiempo+4)
                self.cola.rafaga.append(tiempo-self.cola.comienzo[-1])
                self.cola.rafaga.append(self.cola.rafaga[0]-(tiempo-self.cola.comienzo[-1]))
                self.cola.bloqueo.append(0)
                self.dispatcher.bloqueados.append(self.cola)
            else:
                return
            self.cola=None
        p=self.dispatcher.get(tiempo)
        if p is None:
            return
        p.comienzo.append(tiempo)
        p.final=p.comienzo[-1]+p.rafaga[-1]
        self.cola=p
        return(p)