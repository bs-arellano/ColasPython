class Proceso:
    comienzo: int
    final: int
    def __init__(self, id, t, p, r, b=0):
        self.nombre=id
        self.llegada=[t]
        self.prioridad=p
        self.rafaga=[r]
        self.bloqueo=[b]
        self.comienzo=[]
        self.final=None
        self.retorno=None
        self.espera=None
    def __str__(self) -> str:
        return f"{self.nombre} con tiempo de llegada:{self.llegada}, prioridad:{self.prioridad}, rafaga:{self.rafaga}, comienzo:{self.comienzo}, final:{self.final}, retorno:{self.retorno}, espera: {self.espera}, bloqueo:{self.bloqueo}"