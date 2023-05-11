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
    def get(self, t)->Proceso:
        if len(self.nuevos)>0:
            #print(f"[{t}] proceso en nuevos {len(self.nuevos)}")
            for p in sorted(self.nuevos,key=lambda x:x.llegada[0]):
                if p.llegada[0]<=t:
                    #print(f"Moviendo {p} a listos en {t}")
                    self.listos.append(p)
                    self.nuevos.remove(p)
        if len(self.bloqueados)>0:
            #print(f"[{t}] proceso en bloqueados {len(self.bloqueados)}")
            for p in sorted(self.bloqueados, key=lambda x:x.llegada[-1]):
                if p.llegada[-1]<=t:
                    #print(f"Moviendo {p} a listos en {t}")
                    self.listos.append(p)
                    self.bloqueados.remove(p)
                
        if len(self.listos)>0:
            self.listos.sort(key=lambda x: x.prioridad,reverse=True)
            #print(f"[{t}] listos:")
            return self.listos.pop()