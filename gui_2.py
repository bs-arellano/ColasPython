import tkinter as tk
from tkinter import ttk
from procesador import Procesador
from nodo import Nodo

class GUI:
    def __init__(self, cpu):
        self.root = tk.Tk()
        self.crear_elementos()
        
    def crear_elementos(self):
        #Frames
        self.frame_tabla = tk.Frame(master=self.root)
        self.frame_tabla.grid(row=0, column=0)
        self.frame_semaforo = tk.Frame(master=self.root)
        self.frame_semaforo.grid(row=0, column=1)
        self.frame_gantt = tk.Frame(master=self.root)
        self.frame_gantt.grid(row=1, column=0)
        self.frame_botones = tk.Frame(master=self.root)
        self.frame_botones.grid(row=2, column=0)
        #Tabla
        self.tabla = ttk.Treeview(master=self.frame_tabla, columns=['proceso', 'llegada', 'rafaga', 'comienzo', 'final', 'retorno', 'espera'])
        self.tabla.column("#0", width=0, stretch=0)
        self.tabla.heading(column='proceso', text="Proceso")
        self.tabla.heading(column='llegada', text="Tiempo de llegada")
        self.tabla.heading(column='rafaga', text="Rafaga")
        self.tabla.heading(column='comienzo', text="Tiempo de comienzo")
        self.tabla.heading(column='final', text="Tiempo final")
        self.tabla.heading(column='retorno', text="Tiempo de retorno")
        self.tabla.heading(column='espera', text="Tiempo de espera")
        self.tabla.pack()
        #Semaforo
        self.canvas_semaforo = tk.Canvas(master=self.frame_semaforo, width=100, height=100)
        self.semaforo = self.canvas_semaforo.create_oval(25, 25, 50, 50, fill='red')
        self.canvas_semaforo.pack()
        #Boton Agregar
        boton_agregar_nodo = tk.Button(self.frame_botones, text="Agregar nodo", command=self.crear_nodo)
        boton_agregar_nodo.pack()

    def crear_nodo(self):
        self.tabla.insert(parent="", index="end", values=("A","0","0","0","0","0","0"))
        self.tabla.pack()

    def ejecutar(self):
        self.root.mainloop()