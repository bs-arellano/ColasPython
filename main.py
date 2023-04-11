import tkinter as tk
import time
import random

class Nodo:
    def __init__(self, nombre, transacciones, puntero=None):
        self.nombre = nombre
        self.transacciones = transacciones
        self.puntero: Nodo = puntero
    def add_nodo(self, nodo):
        if self.puntero is None:
            self.puntero = nodo
        else:
            self.puntero.add_nodo(nodo)

class Procesador:
    cola: Nodo = None
    def __init__(self, capacidad, cola: Nodo=None):
        self.capacidad = capacidad
        self.cola = cola
    def agregar_nodo(self, nodo: Nodo):
        if self.cola is None:
            self.cola = nodo
        else:
            self.cola.add_nodo(nodo)
    def atender(self):
        if self.cola is None:
            print("No quedan nodos")
            return -1, ''
        elif self.cola.transacciones <= self.capacidad:
            print(f"Nodo: {self.cola.nombre}, Transacciones: {self.cola.transacciones}")
            self.cola.transacciones = 0
            self.cola = self.cola.puntero
            return 0, ''
        else:
            print(f"Nodo: {self.cola.nombre}, Transacciones: {self.cola.transacciones} Capacidad: {self.capacidad}")
            self.cola.transacciones -= self.capacidad
            ultimo = self.cola
            self.cola = self.cola.puntero
            return ultimo.transacciones, ultimo.nombre

class GUI:
    nodos = []
    id = 1
    def __init__(self, cpu):
        self.procesador: Procesador = cpu
        self.root = tk.Tk()
        self.width = 800
        self.height = 400
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.crear_elementos()
    def crear_elementos(self):
        self.ob_procesador = self.canvas.create_oval(50, (self.height//2)-20, 90, (self.height//2)+20, fill='red')
        boton_agregar_nodo = tk.Button(self.root, text="Agregar nodo")
        boton_agregar_nodo.pack(side=tk.LEFT, padx=10, pady=10)
        boton_agregar_nodo.config(command=self.crear_nodo)
        boton_simular = tk.Button(self.root, text="Simular")
        boton_simular.pack(side=tk.LEFT, padx=10, pady=10)
        boton_simular.config(command=self.simular)
    def crear_nodo(self, n="", t=0):
        if t==0:
            t=random.randint(1, 10)
        if n=="":
            n=f"nodo {self.id}"
            self.id+=1
        nombre = n
        transacciones = t
        nodo = Nodo(nombre=nombre, transacciones=transacciones)
        self.procesador.agregar_nodo(nodo)
        if len(self.nodos) > 0:
            x1, y1, x2, y2 = self.canvas.coords(self.nodos[-1])
        else:
            x1, y1 = 50, (self.height//2)-20
        ob_nodo = self.canvas.create_rectangle(x1+40+20, y1, x1+20+40+40, y1+40, fill='blue')
        self.nodos.append(ob_nodo)
    def simular(self):
        while self.procesador.cola is not None:
            self.canvas.itemconfig(self.ob_procesador, fill='orange')
            self.canvas.itemconfig(self.nodos[0], fill='green')
            self.root.update()
            if self.procesador.cola.transacciones>self.procesador.capacidad:
                time.sleep(1)
            else:
                time.sleep(self.procesador.cola.transacciones/5)
            t, n = self.procesador.atender()
            if t > 0:
                self.crear_nodo(n, t)
            self.canvas.delete(self.nodos[0])
            self.nodos.pop(0)
            for nodo in self.nodos:
                self.canvas.move(nodo, -60, 0)
        self.canvas.itemconfig(self.ob_procesador, fill='red')

    def ejecutar(self):
        self.root.mainloop()
if __name__=='__main__':
    procesador = Procesador(5)
    gui = GUI(procesador)
    gui.ejecutar()