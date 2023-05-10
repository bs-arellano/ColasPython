class Nodo:
    #Metodo constructor
    def __init__(self, nombre, transacciones, puntero=None):
        self.nombre = nombre
        self.transacciones = transacciones
        self.puntero: Nodo = puntero
        print(f"[Nuevo nodo] Nombre: {nombre}, transacciones: {transacciones}")
    #Añade un nodo al final
    def add_nodo(self, nodo):
        if not isinstance(self.puntero, Nodo):
            self.puntero = nodo
        else:
            self.puntero.add_nodo(nodo)

class Proceso:
    def __init__(self, nombre, t_llegada, prioridad, rafaga, bloqueo):
        self.nombre=nombre
        self.prioridad=prioridad
        self.rafaga=rafaga
        self.t_llegada=t_llegada
        self.bloqueo=bloqueo