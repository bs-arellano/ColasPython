from procesador import Procesador, Proceso, Dispatcher
import tkinter as tk
from tkinter import ttk
import threading
import time

class GUI:
    def __init__(self, cpu: Procesador):
        #constantes
        self.width=800
        self.height=450
        self.rows=1
        self.t_range=40
        self.speed=4
        self.t = 0
        #objetos
        self.simulaciones = []
        self.simulaciones.append(threading.Thread(target=self.simular))
        self.procesos = []
        #Ventana principal
        self.root = tk.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        #print(self.screen_width, self.screen_height)
        self.root.geometry(f"{self.width}x{self.height+170}+{(self.screen_width-self.width)//2}+{((self.screen_height-self.height)//2)-100}")
        self.root.title("Round Robin")
        self.cpu=cpu
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
        self.tabla.column('proceso', width=self.width//8, stretch=False)
        self.tabla.heading(column='llegada', text="Tiempo de llegada")
        self.tabla.column('llegada', width=self.width//8, stretch=False)
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
        self.tabla.pack()
        #Semaforo
        self.canvas_semaforo = tk.Canvas(master=self.frame_semaforo, width=100, height=100)
        self.semaforo = self.canvas_semaforo.create_oval(10,10,90,90, fill='green')
        self.label_semaforo = self.canvas_semaforo.create_text(40, 40, text="0")
        self.canvas_semaforo.pack()
        #Gantt
        self.canvas_gantt = tk.Canvas(master=self.frame_gantt, width=self.width, height=self.height//2, background='white')
        self.dibujar_diagrama()
        self.canvas_gantt.pack()
        #Boton Agregar
        boton_agregar_nodo = tk.Button(self.frame_botones, text="Agregar nodo", command=self.ventana_datos)
        boton_agregar_nodo.pack(side="left")
        #Boton Simular
        lamda_simular = lambda: self.simulaciones[-1].start() if len(self.procesos)>0 else None
        boton_simular = tk.Button(self.frame_botones, text="Simular", command=lamda_simular)
        boton_simular.pack(side="left")
        #Boton Reiniciar
        boton_reiniciar = tk.Button(self.frame_botones, text="Reiniciar", command=self.reiniciar)
        boton_reiniciar.pack(side="left")
        #Boton Bloquear
        boton_bloquear = tk.Button(self.frame_semaforo, text="Bloquear", command=lambda: self.cpu.bloquear(self.t))
        boton_bloquear.pack(side="left")
        #Boton Limpiar
        boton_limpiar = tk.Button(self.frame_botones, text="Limpiar", command=self.limpiar)
        boton_limpiar.pack(side="left")

    def ventana_datos(self):
        #Ventana emergente
        data_window=tk.Toplevel(master=self.root)
        data_window.geometry(f"300x300+{(self.screen_width-300)//2}+{(self.screen_height-300)//2}")
        #ID
        tk.Label(data_window, text="Id del nodo").pack()
        id_input=tk.Entry(master=data_window)
        id_input.pack()
        #Llegada
        tk.Label(master=data_window, text="Tiempo de llegada").pack()
        t_in_input=tk.Entry(master=data_window)
        t_in_input.pack()
        #Rafaga
        tk.Label(master=data_window, text="Rafaga").pack()
        raf_input=tk.Entry(master=data_window)
        raf_input.pack()
        #Guardar
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

    def dibujar_tarea(self, i, nombre, llegada, final, color):
        x0=10+((self.width-20)//self.t_range)*llegada
        x1=10+((self.width-20)//self.t_range)*final
        y0=(((self.height//4)//self.rows)*(i+1))-10
        self.canvas_gantt.create_rectangle(x0,y0,x1,y0+20,fill=color)
        self.canvas_gantt.create_text(x0+10, y0+10, text=nombre)

    def ejecutar(self):
        self.root.mainloop()

    def crear_nodo(self, id, t0, raf):
        #Validacion
        if id=="" or t0=="" or raf=="":
            return
        try:
            t0 = int(t0)
            raf = int(raf)
        except:
            return
        if len(self.cpu.dispatcher.nuevos)>0 and t0<sorted(self.cpu.dispatcher.nuevos, key=lambda x:x.llegada[0])[-1].llegada[0]:
            return
        #Crea el proceso y lo añade a CPU
        p = Proceso(id,t0,raf)
        self.procesos.append(p)
        self.cpu.agregar_proceso(p)

    def simular(self):
        self.t=0
        self.rows=len(self.procesos)
        #Si hay procesos sin finalizar
        while self.cpu.cola!=None or len(self.cpu.dispatcher.nuevos)>0 or len(self.cpu.dispatcher.listos)>0 or len(self.cpu.dispatcher.bloqueados)>0:
            self.cpu.atender(self.t)
            self.actualizar()
            if self.cpu.cola is None:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="green")
                self.canvas_semaforo.itemconfig(self.label_semaforo, text=self.t)
            else:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="red")
                self.canvas_semaforo.itemconfig(self.label_semaforo, text=f"{self.t} {self.cpu.cola.nombre}")
            self.canvas_semaforo.update()
            time.sleep(1/self.speed)
            self.t+=1

    def reiniciar(self):
        #Resetea CPU
        self.cpu.dispatcher = Dispatcher()
        self.cpu.cola=None
        for p in self.procesos:
            p.ejecutada = []
            p.comienzo = []
            p.final = "-"
            p.retorno = "-"
            p.espera= "-"
            self.cpu.agregar_proceso(p)
        #Borra tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        #Borra gantt
        self.canvas_gantt.delete('all')
        self.rows=1
        self.dibujar_diagrama()
        #Semaforo
        self.canvas_semaforo.itemconfig(self.semaforo, fill="green")
        self.canvas_semaforo.itemconfig(self.label_semaforo, text="0")
        #Termina hilo
        if self.simulaciones[-1].is_alive():
            self.simulaciones[-1].join()
        self.simulaciones.append(threading.Thread(target=self.simular))
    
    def actualizar(self):
        #Borra tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        #Actualiza
        for i, p in enumerate(self.procesos):
            if len(p.llegada)<=0:
                continue
            self.tabla.insert(parent="", index="end", values=[p.nombre, p.llegada[0], p.rafaga, p.comienzo, p.final, p.retorno, p.espera])
            if self.cpu.cola is p:
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, 'green')
            elif self.cpu.dispatcher.listos.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, 'yellow')
            elif self.cpu.dispatcher.bloqueados.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, 'red')

    def limpiar(self):
        self.procesos = []
        self.reiniciar()