from proceso import Proceso
from dispatcher import Dispatcher, DispatcherRR, DispatcherSRTF, DispatcherPrioridades

class Procesador:
    def __init__(self):
       self.round_robin = DispatcherRR()
       self.srtf = DispatcherSRTF()
       self.prioridades = DispatcherPrioridades()
       self.cola:Proceso=None
       self.current_dispatcher: Dispatcher = None
       self.bloqueos_pendientes = []

    def agregar_proceso(self, process: Proceso, dispatcher: Dispatcher):
        dispatcher.add(process)
        print(f'\033[96mAgregado {process} en {dispatcher} \033[0m')

    def bloquear(self, tiempo):
        if self.cola is None:
            return
        self.cola.llegada.append(tiempo+4)
        self.cola.ejecutada.append(0)
        self.current_dispatcher.bloqueados.append(self.cola)
        print(f'\033[31m[{tiempo}] Bloqueado {self.cola} en {self.current_dispatcher} \033[0m')
        self.cola=None
        self.current_dispatcher=None
    
    def expulsar(self, dispatcher: Dispatcher, tiempo):
        if self.cola is None:
            return
        self.cola.llegada.append(tiempo)
        dispatcher.listos.append(self.cola)
        print(f'\033[91m[{tiempo}] Expulsado {self.cola} en {dispatcher} \033[0m')
        self.cola=None

    def terminar(self, dispatcher: Dispatcher, tiempo):
        if self.cola is None:
            return
        self.cola.final=tiempo
        self.cola.retorno=self.cola.final-self.cola.llegada[0]
        self.cola.espera=self.cola.retorno-self.cola.rafaga
        dispatcher.terminados.append(self.cola)
        print(f'\033[35m[{tiempo}] Terminado {self.cola} en {dispatcher} \033[0m')
        self.cola = None
        self.current_dispatcher=None

    def atender(self, tiempo):
        #Actualiza cola de listos
        for p in self.round_robin.check(tiempo):
            self.round_robin.listos.append(p)
        for p in self.srtf.check(tiempo):
            p.llegada.append(tiempo)
            p.dispatcher='Round Robin'
            self.round_robin.listos.append(p)
            print(f'\033[93m[{tiempo}] Moviendo {p.nombre} por inanicion en rr \033[0m')
        for p in self.prioridades.check(tiempo):
            p.llegada.append(tiempo)
            p.dispatcher='SRTF'
            self.srtf.listos.append(p)
            print(f'\033[93m[{tiempo}] Moviendo {p.nombre} por inanicion en prioridades \033[0m')
        #Si el proceso finaliza lo mueve a terminados
        if self.cola is not None and self.cola.rafaga==sum(self.cola.ejecutada):
            self.terminar(self.current_dispatcher, tiempo)
        #Revisa bloqueos
        if self.cola is not None and len(self.bloqueos_pendientes)>0:
            self.bloqueos_pendientes.pop()
            self.bloquear(tiempo)
        #Establece dispatcher a usar
        if self.current_dispatcher is None:
            if len(self.round_robin.listos)>0:
                self.current_dispatcher = self.round_robin
            elif len(self.srtf.listos)>0:
                self.current_dispatcher = self.srtf
            elif len(self.prioridades.listos)>0:
                self.current_dispatcher = self.prioridades
            else:
                return
        #Revisa si un dispatcher superior tiene procesos
        else:
            if len(self.round_robin.listos)>0 and (isinstance(self.current_dispatcher, (DispatcherSRTF, DispatcherPrioridades))):
                self.expulsar(self.current_dispatcher, tiempo)
                self.current_dispatcher = self.round_robin
            elif len(self.srtf.listos)>0 and (isinstance(self.current_dispatcher, DispatcherPrioridades)):
                self.expulsar(self.current_dispatcher, tiempo)
                self.current_dispatcher = self.srtf
        #Obtiene el proceso a ejecutar
        self.cola=self.current_dispatcher.get(self.cola, tiempo)
        print(f'[{tiempo}] Cola: {self.cola}, Dispatcher: {self.current_dispatcher} \033[0m')
        #Aumenta en 1 la rafaga ejecutada
        if self.cola is not None:
            self.cola.ejecutada[-1]+=1
            print(f"\033[32m[{tiempo}] Atendiendo {self.cola} \033[0m")
        
    def pendiente(self)->bool:
        pendiente=False
        if len(self.round_robin.nuevos)>0:
            pendiente=True
        if len(self.round_robin.listos)>0:
            pendiente=True
        if len(self.round_robin.bloqueados)>0:
            pendiente=True
        if len(self.srtf.nuevos)>0:
            pendiente=True
        if len(self.srtf.listos)>0:
            pendiente=True
        if len(self.srtf.bloqueados)>0:
            pendiente=True
        if len(self.prioridades.nuevos)>0:
            pendiente=True
        if len(self.prioridades.listos)>0:
            pendiente=True
        if len(self.prioridades.bloqueados)>0:
            pendiente=True
        return pendiente    