class Proceso:
    def __init__(self, id, t, r, dispatcher, prioridad=0):
        self.nombre=id
        self.llegada=[t]
        self.rafaga=r
        self.prioridad = prioridad
        self.ejecutada=[0]
        self.comienzo=[]
        self.dispatcher=dispatcher
        self.final="-"
        self.retorno="-"
        self.espera="-"
    def __str__(self) -> str:
        return f"{self.nombre} con tiempo de llegada:{self.llegada}, rafaga:{self.rafaga} ejecutada:{self.ejecutada}, comienzo: {self.comienzo}, prioridad: {self.prioridad}, terminado: {self.final}"