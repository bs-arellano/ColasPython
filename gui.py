from procesador import Procesador, Proceso
import tkinter as tk
from tkinter import ttk
import threading
import time

class GUI:
    def __init__(self, cpu: Procesador):
        #constantes
        self.width=800
        self.height=500
        self.rows=1
        self.t_range=40
        #objetos
        self.simulacion = threading.Thread(target=self.simular)
        self.root = tk.Tk()
        self.root.title("Prioridades")
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
        self.tabla = ttk.Treeview(master=self.frame_tabla, columns=['proceso', 'llegada', 'prioridad', 'rafaga', 'comienzo', 'final', 'retorno', 'espera', 'bloqueo'])
        self.tabla.column("#0", width=0, stretch=0)
        self.tabla.heading(column='proceso', text="Proceso")
        self.tabla.column('proceso', width=self.width//8, stretch=False)
        self.tabla.heading(column='llegada', text="Tiempo de llegada")
        self.tabla.column('llegada', width=self.width//8, stretch=False)
        self.tabla.heading(column='prioridad', text="Prioridad")
        self.tabla.column('prioridad', width=self.width//8, stretch=False)
        self.tabla.heading(column='rafaga', text="Rafaga")
        self.tabla.column('rafaga', width=self.width//8, stretch=False)
        self.tabla.heading(column='comienzo', text="Tiempo de comienzo")
        self.tabla.column('comienzo', width=self.width//8, stretch=False)
        self.tabla.heading(column='final', text="Tiempo final")
        self.tabla.column('final', width=self.width//8, stretch=False)
        self.tabla.heading(column='retorno', text="Tiempo de retorno")
        self.tabla.column('retorno', width=self.width//8, stretch=False)
        self.tabla.heading(column='espera', text="Tiempo de espera")
        self.tabla.column('espera', width=self.width//8, stretch=False)
        self.tabla.heading(column='bloqueo', text="Bloqueo")
        self.tabla.column('bloqueo', width=self.width//8, stretch=False)
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
        boton_simular = tk.Button(self.frame_botones, text="Simular", command=self.simulacion.start)
        boton_simular.pack()

    def ventana_datos(self):
        #Ventana emergente
        data_window=tk.Toplevel(master=self.root)
        data_window.geometry("300x300")
        tk.Label(data_window, text="Id del nodo").pack()
        id_input=tk.Entry(master=data_window)
        id_input.pack()
        tk.Label(master=data_window, text="Tiempo de llegada").pack()
        t_in_input=tk.Entry(master=data_window)
        t_in_input.pack()
        tk.Label(data_window, text="Prioridad").pack()
        prioridad_input=tk.Entry(master=data_window)
        prioridad_input.pack()
        tk.Label(master=data_window, text="Rafaga").pack()
        raf_input=tk.Entry(master=data_window)
        raf_input.pack()
        tk.Label(master=data_window, text="Bloqueo").pack()
        bloq_input=tk.Entry(master=data_window)
        bloq_input.pack()
        tk.Button(master=data_window, text="Guardar datos", command=lambda: [self.crear_nodo(id_input.get(), t_in_input.get(), prioridad_input.get(), raf_input.get(), bloq_input.get()), data_window.destroy()]).pack()

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

    def dibujar_tarea(self, i, nombre, llegada, final, color):
        x0=10+((self.width-20)//self.t_range)*llegada
        x1=10+((self.width-20)//self.t_range)*final
        y0=(((self.height//2)//self.rows)*(i+1))-10
        self.canvas_gantt.create_rectangle(x0,y0,x1,y0+20,fill=color)
        self.canvas_gantt.create_text(x0+10, y0+10, text=nombre)

    def ejecutar(self):
        self.root.mainloop()

    def crear_nodo(self, id, t0, pr, raf, bloq):
        #Validacion
        if id=="" or t0=="" or pr=="" or raf=="" or bloq=="":
            return
        try:
            t0 = int(t0)
            pr=int(pr)
            raf = int(raf)
            bloq = int(bloq)
        except:
            return
        if len(self.cpu.dispatcher.nuevos)>0 and t0<sorted(self.cpu.dispatcher.nuevos, key=lambda x:x.llegada)[-1].llegada[0]:
            return
        p = Proceso(id,t0,pr,raf,bloq)
        self.cpu.agregar_proceso(p)

    def simular(self):
        t=0
        while self.cpu.cola!=None or len(self.cpu.dispatcher.nuevos)>0 or len(self.cpu.dispatcher.listos)>0 or len(self.cpu.dispatcher.bloqueados)>0:
            p=self.cpu.atender(t)
            if self.cpu.cola is None:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="green")
            else:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="red")
            self.canvas_semaforo.update()
            time.sleep(1)
            t+=1
        print("Resultados")
        for i, p in enumerate(self.cpu.dispatcher.terminados):
            if p is not None:
                print(p)
                self.tabla.insert(parent="", index="end", values=(p.nombre, p.llegada[0], p.prioridad, p.rafaga[0], p.comienzo, p.final, p.retorno, p.espera, p.bloqueo[0]))
                self.rows+=1
                if len(p.comienzo)>1:
                    for j in range(len(p.comienzo)):
                        self.dibujar_tarea(i, p.nombre, p.comienzo[j], p.comienzo[j]+p.rafaga[j+1], 'green')
                else:
                    self.dibujar_tarea(i, p.nombre, p.comienzo[0], p.comienzo[0]+p.rafaga[0], 'green')
            self.dibujar_diagrama