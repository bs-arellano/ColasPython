from proceso import Proceso

class Dispatcher:
    def __init__(self):
        self.nuevos = []
        self.listos = []
        self.bloqueados = []
        self.terminados=[]
        self.t_inanicion = 20
    def add (self, proceso: Proceso):
        self.nuevos.append(proceso)
    def check(self, t) -> list:
        #Revisa por procesos nuevos
        if len(self.nuevos)>0:
            for p in sorted(self.nuevos, key=lambda x: x.llegada[0]):
                if p.llegada[0]<=t:
                    self.listos.append(p)
                    self.nuevos.remove(p)
        #Revisa por procesos bloquados
        if len(self.bloqueados)>0:
            for p in sorted(self.bloqueados, key=lambda x:x.llegada[-1]):
                if p.llegada[-1]<=t:
                    self.listos.append(p)
                    self.bloqueados.remove(p)
        #Revisa por procesos en inanición
        inanicion = []
        if len(self.listos)>0:
            for i, p in enumerate(self.listos):
                if (t-p.llegada[-1])>self.t_inanicion:
                    self.listos.pop(i)
                    inanicion.append(p)
        return inanicion
        
    def get(self, p: Proceso, t: int):
        pass
    def __str__(self) -> str:
        return 'common'

class DispatcherRR(Dispatcher):
    def __init__(self):
        super().__init__()
        self.quantum = 5
    def add(self, proceso: Proceso):
        super().add(proceso)
    def check(self, t) -> list:
        return super().check(t)                    
    def get(self, p: Proceso, t: int)->Proceso:
        if p is not None:
            #Revisa si el proceso supera el quantum y lo expulsa
            if p.ejecutada[-1] < self.quantum:
                return p
            else:
                p.llegada.append(t)
                p.ejecutada.append(0)
                self.listos.append(p)
                print(f'\033[91m[{t}] Expulsado {p} en rr\033[0m')
        #Elige el proceso por FIFO
        if len(self.listos)>0:
            self.listos.sort(key=lambda x: x.llegada[-1])
            p_alt: Proceso = self.listos.pop(0)
            p_alt.comienzo.append(t)
            return p_alt
    def __str__(self) -> str:
        return 'rr'

class DispatcherSRTF(Dispatcher):
    def __init__(self):
        super().__init__()
    def add(self, proceso: Proceso):
        super().add(proceso)
    def check(self, t) -> list:
        return super().check(t)  
    def get(self, p: Proceso, t: int)->Proceso:
        if len(self.listos)<=0:
            return p
        self.listos.sort(key=lambda x: x.rafaga-sum(x.ejecutada))
        p_alt: Proceso = self.listos.pop(0)
        if p is None:
            p_alt.comienzo.append(t)
            return p_alt
        elif (p.rafaga-sum(p.ejecutada))>(p_alt.rafaga-sum(p_alt.ejecutada)):
            p.llegada.append(t)
            p.ejecutada.append(0)
            self.listos.append(p)
            print(f'\033[91m[{t}] Expulsado {p} en srtf\033[0m')
            p_alt.comienzo.append(t)
            return p_alt
        else:
            self.listos.append(p_alt)
            return p
    def __str__(self) -> str:
        return 'srtf'
    
class DispatcherPrioridades(Dispatcher):
    def __init__(self):
        super().__init__()
    def add(self, proceso: Proceso):
        super().add(proceso)
    def check(self, t) -> list:
        return super().check(t)
    def get(self, p: Proceso, t: int):
        if len(self.listos)<0:
            return p
        self.listos.sort(key=lambda x: (x.prioridad, x.llegada[-1]))
        if p is None:
            p_alt: Proceso = self.listos.pop(0)
            p_alt.comienzo.append(t)
            return p_alt
        else:
            return p
    def __str__(self) -> str:
        return 'prioridades'