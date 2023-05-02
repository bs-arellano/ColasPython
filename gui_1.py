import tkinter as tk
import time
import random

from procesador import Procesador
from nodo import Nodo

class GUI:
    nodos = []
    textos = []
    log = "Registro"
    procesador: Procesador
    id = 1
    #Constructor
    def __init__(self, cpu):
        self.procesador: Procesador = cpu
        self.root = tk.Tk()
        self.width = 800
        self.height = 400
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.crear_elementos()
    def crear_elementos(self):
        #Consola
        self.consola = self.canvas.create_text(600, self.height/2, text=self.log)
        #Crea representacion del procesador
        self.ob_procesador = self.canvas.create_oval(50, (self.height//2)-20, 90, (self.height//2)+20, fill='red')
        #Boton para agregar nodo
        boton_agregar_nodo = tk.Button(self.root, text="Agregar nodo")
        boton_agregar_nodo.pack(side=tk.LEFT, padx=10, pady=10)
        boton_agregar_nodo.config(command=self.crear_nodo)
        #Boton para simular
        boton_simular = tk.Button(self.root, text="Simular")
        boton_simular.pack(side=tk.LEFT, padx=10, pady=10)
        boton_simular.config(command=self.simular)
    #crear_nodo(identificador, numero_transacciones)
    def crear_nodo(self, n="", t=0):
        if t==0:
            t=random.randint(1, 10)
        if n=="":
            n=f"nodo_{self.id}"
            self.id+=1
        nombre = n
        transacciones = t
        nodo = Nodo(nombre=nombre, transacciones=transacciones, puntero=self.procesador)
        self.log += f"\n[Nuevo nodo] Nombre: {nombre}, transacciones: {transacciones}"
        self.canvas.itemconfig(self.consola, text=self.log)
        #Agrega el nodo al procesador
        self.procesador.agregar_nodo(nodo)
        #Representacion del nodo alineada
        if len(self.nodos) > 0:
            x1, y1, x2, y2 = self.canvas.coords(self.nodos[-1])
        else:
            x1, y1 = 50, (self.height//2)-20
        ob_nodo = self.canvas.create_rectangle(x1+60, y1, x1+100, y1+40, fill='blue')
        txt_nodo = self.canvas.create_text(x1+75,y1-10,text=t)
        #Añade el nodo a la lista de nodos
        self.nodos.append(ob_nodo)
        self.textos.append(txt_nodo)
    def simular(self):
        #Si el procesador tiene nodos los atiende
        while isinstance(self.procesador.cola, Nodo):
            #Cambia colores
            self.canvas.itemconfig(self.ob_procesador, fill='orange')
            self.canvas.itemconfig(self.nodos[0], fill='green')
            self.log += f"\n[Atendiendo] Nodo: {self.procesador.cola.nombre}, transacciones: {self.procesador.cola.transacciones}"
            self.canvas.itemconfig(self.consola, text=self.log)
            self.root.update()
            #El numero de transacciones es mayor a la capacidad
            if self.procesador.cola.transacciones>self.procesador.capacidad:
                time.sleep(self.procesador.capacidad)
            #El numero de transacciones es menor a la capacidad
            else:
                time.sleep(self.procesador.cola.transacciones)
            #atiende al nodo y recibe (si lo hay) el faltante de transacciones
            self.canvas.itemconfig(self.consola, text=self.log)
            t, n = self.procesador.atender()
            if t > 0:
                #Crea nodo al final con las faltantes
                self.crear_nodo(n, t)
            #Borra el nodo despues de ser atendido
            self.canvas.delete(self.nodos[0])
            self.nodos.pop(0)
            self.canvas.delete(self.textos[0])
            self.textos.pop(0)
            #mueve los nodos al procesador
            for nodo in self.nodos:
                self.canvas.move(nodo, -60, 0)
            for texto in self.textos:
                self.canvas.move(texto, -60, 0)
        #Cuando no hay mas nodos acaba
        self.canvas.itemconfig(self.ob_procesador, fill='red')

    def ejecutar(self):
        self.root.mainloop()