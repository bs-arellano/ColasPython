from procesador import Procesador, Proceso, Dispatcher, DispatcherRR, DispatcherSRTF, DispatcherPrioridades
import tkinter as tk
from tkinter import ttk
import threading
import time
import os

class GUI:
    def __init__(self, cpu: Procesador):
        #constantes
        self.width=800
        self.height=450
        self.rows=1
        self.t_range=40
        self.speed=4
        self.t = 0
        self.registro_gantt=[]
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
        self.root.title("SRTF")
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
        self.tabla.grid(row=0, column=0)
        #Tablas pequeñas
        self.tabla1 = ttk.Treeview(master=self.frame_tabla, columns=['proceso', 'llegada', 'rafaga'])
        self.tabla1.column("#0", width=0, stretch=0)
        self.tabla1.heading(column='proceso', text="Proceso")
        self.tabla1.column('proceso', width=self.width//8, stretch=False)
        self.tabla1.heading(column='llegada', text="Tiempo de llegada")
        self.tabla1.column('llegada', width=self.width//8, stretch=False)
        self.tabla1.heading(column='rafaga', text="Rafaga")
        self.tabla1.column('rafaga', width=self.width//8, stretch=False)
        self.tabla1.grid(row=0, column=1)
        
        self.tabla2 = ttk.Treeview(master=self.frame_tabla, columns=['proceso', 'llegada', 'rafaga'])
        self.tabla2.column("#0", width=0, stretch=0)
        self.tabla2.heading(column='proceso', text="Proceso")
        self.tabla2.column('proceso', width=self.width//8, stretch=False)
        self.tabla2.heading(column='llegada', text="Tiempo de llegada")
        self.tabla2.column('llegada', width=self.width//8, stretch=False)
        self.tabla2.heading(column='rafaga', text="Rafaga")
        self.tabla2.column('rafaga', width=self.width//8, stretch=False)
        self.tabla2.grid(row=0, column=2)
        
        self.tabla3 = ttk.Treeview(master=self.frame_tabla, columns=['proceso', 'llegada', 'rafaga', 'prioridad'])
        self.tabla3.column("#0", width=0, stretch=0)
        self.tabla3.heading(column='proceso', text="Proceso")
        self.tabla3.column('proceso', width=self.width//8, stretch=False)
        self.tabla3.heading(column='llegada', text="Tiempo de llegada")
        self.tabla3.column('llegada', width=self.width//8, stretch=False)
        self.tabla3.heading(column='rafaga', text="Rafaga")
        self.tabla3.column('rafaga', width=self.width//8, stretch=False)
        self.tabla3.heading(column='prioridad', text="Prioridad")
        self.tabla3.column('prioridad', width=self.width//8, stretch=False)
        self.tabla3.grid(row=0, column=3)
        
        #Semaforo
        self.canvas_semaforo = tk.Canvas(master=self.frame_semaforo, width=100, height=100)
        self.semaforo = self.canvas_semaforo.create_oval(10,10,90,90, fill='#00DFA2')
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
        boton_bloquear = tk.Button(self.frame_semaforo, text="Bloquear", command=lambda: self.cpu.bloqueos_pendientes.append(self.t))
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
        #Rafaga
        tk.Label(master=data_window, text="Rafaga").pack()
        raf_input=tk.Entry(master=data_window)
        raf_input.pack()
        #Diapatcher
        tk.Label(master=data_window, text="Algoritmo").pack()
        dispatcher=ttk.Combobox(master=data_window, values=['Round Robin', 'SRTF', 'Prioridades'], state='readonly')
        dispatcher.current(0)
        dispatcher.pack()
        #Prioridad
        tk.Label(master=data_window, text="Prioridad").pack()
        pr_input=tk.Entry(master=data_window)
        pr_input.pack()
        #Guardar
        tk.Button(master=data_window, text="Guardar datos", command=lambda: [self.crear_nodo(id_input.get(), raf_input.get(), dispatcher.get(), pr_input.get()), data_window.destroy()]).pack()

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
        y0=(((self.height//2)//self.rows)*(i+1))-20
        self.canvas_gantt.create_rectangle(x0,y0,x1,y0+20,fill=color)
        self.canvas_gantt.create_text(x0+10, y0+10, text=nombre)

    def ejecutar(self):
        self.root.mainloop()

    def crear_nodo(self, id, raf, dis, pr):
        #Validacion
        if id=="" or raf=="" or dis=="":
            return
        if pr == "":
            pr="0"
        try:
            raf = int(raf)
            pr = int(pr)
            if raf<=0:
                return
            if dis=='Round Robin':
                dispatcher = self.cpu.round_robin
            elif dis=='SRTF':
                dispatcher = self.cpu.srtf
            elif dis=='Prioridades':
                dispatcher = self.cpu.prioridades
                if pr==0:
                    return
            else:
                return
        except:
            return
        #Crea el proceso y lo añade a CPU
        p = Proceso(id,self.t,raf, dis, pr)
        self.procesos.append(p)
        self.cpu.agregar_proceso(p, dispatcher)
        self.actualizar()

    def simular(self):
        self.t=0
        #Si hay procesos sin finalizar
        while self.cpu.cola!=None or self.cpu.pendiente():
            self.rows=len(self.procesos)
            self.cpu.atender(self.t)
            self.actualizar()
            if self.cpu.cola is None:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="#00DFA2")
                self.canvas_semaforo.itemconfig(self.label_semaforo, text=self.t)
            else:
                self.canvas_semaforo.itemconfig(self.semaforo, fill="#FF0060")
                self.canvas_semaforo.itemconfig(self.label_semaforo, text=f"{self.t} {self.cpu.cola.nombre}")
            self.canvas_semaforo.update()
            time.sleep(1/self.speed)
            self.t+=1

    def reiniciar(self):
        self.t=0
        self.registro_gantt=[]
        os.system('cls' if os.name == 'nt' else 'clear')
        #Resetea CPU
        self.cpu.round_robin = DispatcherRR()
        self.cpu.srtf = DispatcherSRTF()
        self.cpu.prioridades = DispatcherPrioridades()
        self.cpu.current_dispatcher = None
        self.cpu.cola=None
        for p in self.procesos:
            p.llegada = [p.llegada[0]]
            p.ejecutada = [0]
            p.comienzo = []
            p.final = "-"
            p.retorno = "-"
            p.espera= "-"
            if p.dispatcher=='Round Robin':
                self.cpu.agregar_proceso(p, self.cpu.round_robin)
            elif p.dispatcher=='SRTF':
                self.cpu.agregar_proceso(p, self.cpu.srtf)
            elif p.dispatcher=='Prioridades':
                self.cpu.agregar_proceso(p, self.cpu.prioridades)
        #Borra tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for i in self.tabla1.get_children():
            self.tabla1.delete(i)
        for i in self.tabla2.get_children():
            self.tabla2.delete(i)
        for i in self.tabla3.get_children():
            self.tabla3.delete(i)
        #Borra gantt
        self.canvas_gantt.delete('all')
        self.rows=1
        self.dibujar_diagrama()
        #Semaforo
        self.canvas_semaforo.itemconfig(self.semaforo, fill="#00DFA2")
        self.canvas_semaforo.itemconfig(self.label_semaforo, text="0")
        #Termina hilo
        if self.simulaciones[-1].is_alive():
            self.simulaciones[-1].join()
        self.simulaciones.append(threading.Thread(target=self.simular))
    
    def actualizar(self):
        #Borra tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for i in self.tabla1.get_children():
            self.tabla1.delete(i)
        for i in self.tabla2.get_children():
            self.tabla2.delete(i)
        for i in self.tabla3.get_children():
            self.tabla3.delete(i)
        self.canvas_gantt.delete('all')
        self.rows=len(self.procesos)
        self.dibujar_diagrama()
        #Actualiza
        for i, p in enumerate(self.procesos):
            if len(p.llegada)<=0:
                continue
            #Tabla General
            self.tabla.insert(parent="", index="end", values=[p.nombre, p.llegada[0], p.rafaga, p.comienzo, p.final, p.retorno, p.espera])
            #Tabla RoundRobin
            if p.dispatcher == 'Round Robin':
                self.tabla1.insert(parent="", index="end", values=[p.nombre, p.llegada[0], p.rafaga])
            #Tabla SRTF
            if p.dispatcher == 'SRTF':
                self.tabla2.insert(parent="", index="end", values=[p.nombre, p.llegada[0], p.rafaga])
            #Tabla Prioridades
            if p.dispatcher == 'Prioridades':
                self.tabla3.insert(parent="", index="end", values=[p.nombre, p.llegada[0], p.rafaga, p.prioridad])
            #Procesos en Registro
            for p_log, t_log, c_log in self.registro_gantt:
                if p.nombre == p_log:
                    self.dibujar_tarea(i, p_log, t_log, t_log+1, c_log)
            #Proceso en seccion critica
            if self.cpu.cola is p:
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#79B8D1')
                self.registro_gantt.append((p.nombre, self.t, '#79B8D1'))
            #Proceso en listos
            elif self.cpu.round_robin.listos.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#A8E4B1')
                self.registro_gantt.append((p.nombre, self.t, '#A8E4B1'))
            elif self.cpu.srtf.listos.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#AEF4A4')
                self.registro_gantt.append((p.nombre, self.t, '#AEF4A4'))
            elif self.cpu.prioridades.listos.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#6BCB77')
                self.registro_gantt.append((p.nombre, self.t, '#6BCB77'))
            #Procesos bloqueados
            elif self.cpu.round_robin.bloqueados.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#FF0060')
                self.registro_gantt.append((p.nombre, self.t, '#FF0060'))
            elif self.cpu.srtf.bloqueados.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#E36488')
                self.registro_gantt.append((p.nombre, self.t, '#E36488'))
            elif self.cpu.prioridades.bloqueados.__contains__(p):
                self.dibujar_tarea(i, p.nombre, self.t, self.t+1, '#FF6B6B')
                self.registro_gantt.append((p.nombre, self.t, '#FF6B6B'))

    def limpiar(self):
        self.procesos = []
        self.reiniciar()