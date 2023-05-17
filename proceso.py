class Proceso:
    comienzo: int
    final: int
    def __init__(self, id, t, r, e=0):
        self.nombre=id
        self.llegada=[t]
        self.rafaga=r
        self.ejecutada=[e]
        self.comienzo=[]
        self.final="-"
        self.retorno="-"
        self.espera="-"
    def __str__(self) -> str:
        return f"{self.nombre} con tiempo de llegada:{self.llegada}, rafaga:{self.rafaga} ejecutada:{self.ejecutada}, comienzo:{self.comienzo}, final:{self.final}, retorno:{self.retorno}, espera: {self.espera}"