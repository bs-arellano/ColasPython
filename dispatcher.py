from proceso import Proceso
class Dispatcher:
    def __init__(self):
        self.nuevos = []
        self.listos = []
        self.bloqueados = []
        self.terminados=[]
    def add(self, proceso: Proceso):
        print(f"Agregado {proceso}")
        self.nuevos.append(proceso)

    def check(self, t):
        #Mueve los procesos nuevos a listos en el instante t
        if len(self.nuevos)>0:
            for p in sorted(self.nuevos,key=lambda x:x.llegada[0]):
                if p.llegada[0]<=t:
                    self.listos.append(p)
                    self.nuevos.remove(p)

        #Mueve los procesos bloqueados a listos en el instante t
        if len(self.bloqueados)>0:
            for p in sorted(self.bloqueados, key=lambda x:x.llegada[-1]):
                if p.llegada[-1]<=t:
                    self.listos.append(p)
                    self.bloqueados.remove(p)
                    
    def get(self, t)->Proceso:
        #Elige el proceso listo que debe ser ejecutado
        if len(self.listos)>0:
            self.listos.sort(key=lambda x: x.llegada[-1])
            p: Proceso = self.listos.pop(0)
            p.ejecutada.append(0)
            return p