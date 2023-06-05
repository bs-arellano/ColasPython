from procesador import Procesador
from proceso import Proceso
class Test:
    def __init__(self, procesador: Procesador) -> None:
        t = 0
        procesador.agregar_proceso(Proceso('a', t, 6), procesador.round_robin)
        procesador.agregar_proceso(Proceso('b', t, 3), procesador.srtf)
        procesador.agregar_proceso(Proceso('c', t, 3, 1), procesador.prioridades)
        procesador.agregar_proceso(Proceso('d', t, 3, 2), procesador.prioridades)
        for i in range(0, 100):
            if i == 2:
                procesador.agregar_proceso(Proceso('e', i, 7), procesador.round_robin)
            if i == 14:
                procesador.agregar_proceso(Proceso('f', i, 1), procesador.srtf)
            if i == 16:
                procesador.agregar_proceso(Proceso('g', i, 3, 1), procesador.prioridades)
            if i == 25:
                procesador.agregar_proceso(Proceso('a', i, 6), procesador.srtf)
            
            procesador.atender(i)

