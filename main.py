import tkinter as tk

class Nodo:   
    def __init__(self, nombre, transacciones, puntero=None):
        self.nombre = nombre
        self.transacciones = transacciones
        self.puntero = puntero
    def add_nodo(self, nodo):
        if self.puntero is None:
            self.puntero = nodo
        else:
            self.puntero.add_nodo(nodo)

class Procesador:
    def __init__(self, capacidad, cola=None):
        self.capacidad = capacidad
        self.cola = cola
    def agregar_nodo(self, nodo):
        if self.cola is None:
            self.cola = nodo
        else:
            self.cola.add_nodo(nodo)
    def atender(self):
        if self.cola is None:
            return
        elif self.cola.transacciones <= self.capacidad:
            self.cola.transacciones = 0
            self.cola = self.cola.puntero
        else:
            self.cola.transacciones -= self.capacidad
            ultimo = self.cola
            self.cola = self.cola.puntero
            self.cola.add_nodo(ultimo)

class GUI:
    def __init__(self, cpu):
        self.root = tk.Tk()
        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.procesador = None
        self.nodos = []
        self.crear_elementos()
        self.cpu = cpu

    def crear_nodo(self):
        pass
        # Crear los nodos como cuadrados azules alineados horizontalmente a la izquierda del procesador
        nodo_lado = 40
        nodo_espacio = 50
        nodo_y = self.canvas_height // 2
        if len(self.nodos)==0:
            nodo_x = 50 + nodo_lado + nodo_espacio
        else:
            x1, y1, x2, y2 = self.canvas.coords(self.nodos[-1])
            nodo_x = x1 + nodo_lado + nodo_espacio
        nodo = self.canvas.create_rectangle(nodo_x, nodo_y - nodo_lado//2, nodo_x + nodo_lado, nodo_y + nodo_lado//2, fill='blue')
        self.cpu.agregar_nodo(Nodo("nodo x", 5))
        self.nodos.append(nodo)

    def crear_elementos(self):
        # Crear el procesador como un círculo rojo en el centro del canvas
        procesador_x = 50
        procesador_y = self.canvas_height // 2
        procesador_radio = 30
        self.procesador = self.canvas.create_oval(procesador_x - procesador_radio, 
                                                  procesador_y - procesador_radio,
                                                  procesador_x + procesador_radio, 
                                                  procesador_y + procesador_radio, 
                                                  fill='red')
        
        # Crear los botones "Agregar nodo" y "Simular" en la parte inferior del canvas
        boton_agregar_nodo = tk.Button(self.root, text="Agregar nodo")
        boton_agregar_nodo.pack(side=tk.LEFT, padx=10, pady=10)
        boton_agregar_nodo.config(command=self.crear_nodo)
        boton_simular = tk.Button(self.root, text="Simular")
        boton_simular.pack(side=tk.LEFT, padx=10, pady=10)
        boton_simular.config(command=self.simular)
    
    def ejecutar(self):
        self.root.mainloop()

    def simular(self):
        pass

if __name__=='__main__':
    procesador = Procesador(5)
    gui = GUI(procesador)
    gui.ejecutar()