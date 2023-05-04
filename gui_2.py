import tkinter as tk
from tkinter import ttk
import threading
import time
from procesador import Procesador
from nodo import Nodo

class GUI:
    tareas = []
    def __init__(self, cpu: Procesador):
        #constantes
        self.width=1000
        self.height=700
        self.rows=1
        self.t_range=40
        #objetos
        self.root = tk.Tk()
        self.root.title("FCFS")
        self.cpu=cpu
        #self.root.resizable(0,0)
        self.crear_elementos()
        
    def crear_elementos(self):
        #Frames
        self.frame_tabla = tk.Frame(master=self.root)
        self.frame_tabla.grid(row=0, column=0)
        self.frame_semaforo = tk.Frame(master=self.root)
        self.frame_semaforo.grid(row=1, column=0)
        self.frame_gantt = tk.Frame(master=self.root)
        self.frame_gantt.grid(row=2, column=0)
        self.frame_botones = tk.Frame(master=self.root)
        self.frame_botones.grid(row=3, column=0)
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
        self.semaforo = self.canvas_semaforo.create_oval(10,10,90,90, fill='green')
        self.label_semaforo = self.canvas_semaforo.create_text(40, 40, text="")
        self.canvas_semaforo.pack()
        #Gantt
        self.canvas_gantt = tk.Canvas(master=self.frame_gantt, width=self.width, height=self.height//2, background='white')
        self.dibujar_diagrama()
        self.canvas_gantt.pack()
        #Boton Agregar
        boton_agregar_nodo = tk.Button(self.frame_botones, text="Agregar nodo", command=self.ventana_datos)
        boton_agregar_nodo.pack()
        #Boton Simular
        boton_simular = tk.Button(self.frame_botones, text="Simular", command=self.simular)
        boton_simular.pack()

    def crear_nodo(self, id, t0, raf):
        #Validacion
        if id=="" and t0=="" and raf=="":
            return
        t0 = int(t0)
        raf = int(raf)
        if len(self.tareas)>0 and t0<self.tareas[-1][1]:
            return
        #Limpia
        self.cpu.cola=None
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        self.canvas_gantt.delete('all')
        self.rows+=1
        self.dibujar_diagrama()
        #Calculos
        self.tareas.append((id, t0, raf))
        self.tareas.sort(key=lambda x: x[1])
        for i, tarea in enumerate(self.tareas):
            nombre = tarea[0]
            llegada = tarea[1]
            rafaga = tarea[2]
            if i==0:
                comienzo=llegada
            elif llegada>self.tareas[i-1][4]:
                comienzo=llegada
            else:
                comienzo=self.tareas[i-1][4]
            final=rafaga+comienzo
            retorno=final-llegada
            espera=retorno-rafaga
            self.tareas[i]=(nombre, llegada, rafaga, comienzo, final, retorno, espera)
            #Crea los nodos
            nodo=Nodo(tarea[0],tarea[2], self.cpu)
            self.cpu.agregar_nodo(nodo)
            #Dibuja los procesos en gantt
            self.dibujar_tarea(i, nombre, llegada, comienzo, final)
            #Añade el proceso a la tabla
            self.tabla.insert(parent="", index="end", values=(nombre,llegada,rafaga,comienzo,final,retorno,espera))
        self.canvas_gantt.update()
        self.tabla.pack()

    def ventana_datos(self):
        #Ventana emergente
        data_window=tk.Toplevel(master=self.root)
        tk.Label(data_window, text="id del nodo").pack()
        id_input=tk.Entry(master=data_window)
        id_input.pack()
        tk.Label(master=data_window, text="Tiempo de llegada").pack()
        t_in_input=tk.Entry(master=data_window)
        t_in_input.pack()
        tk.Label(master=data_window, text="Rafaga").pack()
        raf_input=tk.Entry(master=data_window)
        raf_input.pack()
        tk.Button(master=data_window, text="Guardar datos", command=lambda: [self.crear_nodo(id_input.get(), t_in_input.get(), raf_input.get()), data_window.destroy()]).pack()

    def dibujar_diagrama(self):
        # Dibuja la cuadricula horizontal
        for i in range(1,self.rows+1):
            x0 = 10
            x1 = self.width-10
            y = (((self.height)//2)//self.rows)*i
            #y = 100 * (i+1) + 450  # Ubica las lineas en esa posicion
            self.canvas_gantt.create_line(x0, y, x1, y)
        # Dibuja la cuadricula vertical
        for i in range(self.t_range+1):
            x = 10+((self.width-20)//self.t_range)*i
            y0 = 0
            y1 = self.height//2
            self.canvas_gantt.create_line(x, y0, x, y1)
            self.canvas_gantt.create_text(x+10, y0+10, text=i)

    def dibujar_tarea(self, i, nombre, llegada, espera, final):
        x0=10+((self.width-20)//self.t_range)*llegada
        x1=10+((self.width-20)//self.t_range)*espera
        x2=10+((self.width-20)//self.t_range)*final
        y0=(((self.height//2)//self.rows)*(i+1))-10
        self.canvas_gantt.create_rectangle(x0,y0,x1,y0+20,fill='red')
        self.canvas_gantt.create_rectangle(x1,y0,x2,y0+20,fill='green')
        self.canvas_gantt.create_text(x0+10, y0+10, text=nombre)

    def simular(self):
        while isinstance(self.cpu.cola, Nodo):
            self.canvas_semaforo.itemconfig(self.semaforo, fill='red')
            self.canvas_semaforo.itemconfig(self.label_semaforo, text=self.cpu.cola.nombre)
            self.canvas_semaforo.update()
            espera_semaforo = threading.Thread(target=self.esperar, args=(self.cpu.cola.transacciones,))
            espera_semaforo.start()
            self.cpu.atender()
            espera_semaforo.join()
            self.canvas_semaforo.itemconfig(self.semaforo, fill='green')
            self.canvas_semaforo.itemconfig(self.label_semaforo, text="")
            self.canvas_semaforo.update()

    def esperar(self,t):
        time.sleep(t)

    def ejecutar(self):
        self.root.mainloop()