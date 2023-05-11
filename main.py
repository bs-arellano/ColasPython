'''
from procesador import Procesador, Proceso
import time

cpu=Procesador()
p1=Proceso("A", 1,3,4,1)
p2=Proceso("B", 0,1,4,0)
p3=Proceso("C", 2,1,2,0)
p4=Proceso("D", 10,1,2,0)

cpu.agregar_proceso(p1)
cpu.agregar_proceso(p2)
cpu.agregar_proceso(p3)
cpu.agregar_proceso(p4)

t=0
while True:
    r=cpu.atender(t)
    if r is not None:
        print(f"Ejecutado {r} en tiempo {t}")
    time.sleep(0.1)
    t+=1
'''
from procesador import Procesador
from gui import GUI

cpu=Procesador()
gui=GUI(cpu)
gui.ejecutar()