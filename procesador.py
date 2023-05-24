from proceso import Proceso
from dispatcher import Dispatcher

class Procesador:
    def __init__(self):
       self.dispatcher = Dispatcher()
       self.cola:Proceso=None

    def agregar_proceso(self, p: Proceso):
        self.dispatcher.add(p)

    def bloquear(self,tiempo):
        if self.cola is None:
            return
        print(f"[{tiempo}] Bloqueando {self.cola.nombre}")
        self.cola.llegada.append(tiempo+4)
        self.dispatcher.bloqueados.append(self.cola)
        self.cola=None

    def expulsar(self, tiempo):
        if self.cola is None:
            return
        print(f"[{tiempo}] Expulsando {self.cola.nombre}")
        self.cola.llegada.append(tiempo)
        self.dispatcher.listos.append(self.cola)
        self.cola = None
    
    def terminar(self, tiempo):
        if self.cola is None:
            return
        self.cola.final=tiempo
        self.cola.retorno=self.cola.final-self.cola.llegada[0]
        self.cola.espera=self.cola.retorno-self.cola.rafaga
        self.dispatcher.terminados.append(self.cola)
        print(f"[{tiempo}] Terminando {self.cola.nombre}")
        self.cola = None

    def atender(self, tiempo):
        #Odena colas del dispatcher
        self.dispatcher.check(tiempo)
        #Si el proceso finaliza lo mueve a terminados
        if self.cola is not None and self.cola.rafaga==sum(self.cola.ejecutada):
            self.terminar(tiempo)
        #Obtiene el proceso listo con menor rafaga
        p=self.dispatcher.get()
        #Revisa si hay un proceso con menor rafaga por ejecutar
        if self.cola is not None and p is not None:
            if p.rafaga-sum(p.ejecutada)< self.cola.rafaga-sum(self.cola.ejecutada):
                self.dispatcher.listos.append(self.cola)
                p.comienzo.append(tiempo)
                self.cola = p
            else:
                self.dispatcher.listos.append(p)
        #Revisa si no hay proceso en la seccion critica
        if self.cola is None and p is not None:
            p.comienzo.append(tiempo)
            self.cola = p
        #Aumenta en 1 la rafaga ejecutada
        if self.cola is not None:
            self.cola.ejecutada[-1]+=1
            print(f"[{tiempo}] Atendiendo {self.cola}")