from proceso import Proceso
from dispatcher import Dispatcher

class Procesador:
    def __init__(self, quantum):
       self.dispatcher = Dispatcher()
       self.quantum = quantum
       self.cola:Proceso=None

    def agregar_proceso(self, p: Proceso):
        self.dispatcher.add(p)

    def bloquear(self,tiempo):
        if self.cola is None:
            return
        print(f"[{tiempo}] Bloqueando {self.cola}")
        self.cola.llegada.append(tiempo+4)
        self.dispatcher.bloqueados.append(self.cola)
        self.cola=None

    def expulsar(self, tiempo):
        if self.cola is None:
            return
        print(f"[{tiempo}] Expulsando {self.cola}")
        self.cola.llegada.append(tiempo)
        self.dispatcher.listos.append(self.cola)
        self.cola = None
    
    def terminar(self, tiempo):
        if self.cola is None:
            return
        print(f"[{tiempo}] Terminando {self.cola}")
        self.cola.final=tiempo
        self.cola.retorno=self.cola.final-self.cola.llegada[0]
        self.cola.espera=self.cola.retorno-self.cola.rafaga
        self.dispatcher.terminados.append(self.cola)
        self.cola = None

    def atender(self, tiempo):
        #Si esta ocupado revisa si termino o alcanzo el quantum
        if self.cola is not None:
            self.cola.ejecutada[-1]+=1
            print(f"[{tiempo}] Atendiendo {self.cola}")
            #Si el proceso finaliza lo mueve a terminados
            if self.cola.rafaga==sum(self.cola.ejecutada):
                self.terminar(tiempo)
            #Si alcanza el quantum lo expulsa
            elif self.cola.ejecutada[-1]==self.quantum:
                self.expulsar(tiempo)
        #Si esta libre añade pide un proceso
        if self.cola is None:
            p=self.dispatcher.get(tiempo)
            if p is None:
                return
            p.comienzo.append(tiempo)
            self.cola=p