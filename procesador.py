from nodo import Nodo

class Procesador:
    cola: Nodo = None
    def __init__(self, capacidad, cola=None):
        self.capacidad = capacidad
        self.cola = cola
    def agregar_nodo(self, nodo):
        if not isinstance(self.cola, Nodo):
            self.cola = nodo
        else:
            self.cola.add_nodo(nodo)
    def atender(self):
        if self.cola is None:
            print("No quedan nodos")
            return -1, ''
        else:
            print(f"[Atendiendo] Nodo: {self.cola.nombre}, Transacciones: {self.cola.transacciones}")
            self.cola.transacciones = 0
            self.cola = self.cola.puntero
            return 0, ''
        '''
        elif self.cola.transacciones <= self.capacidad:
            print(f"[Atendiendo] Nodo: {self.cola.nombre}, Transacciones: {self.cola.transacciones}")
            self.cola.transacciones = 0
            self.cola = self.cola.puntero
            return 0, ''
        else:
            print(f"[Atendiendo] Nodo: {self.cola.nombre}, Transacciones: {self.cola.transacciones} Capacidad: {self.capacidad}")
            self.cola.transacciones -= self.capacidad
            ultimo = self.cola
            self.cola = self.cola.puntero
            return ultimo.transacciones, ultimo.nombre
            '''