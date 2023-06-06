from procesador import Procesador
from proceso import Proceso
class Test:
    def __init__(self, procesador: Procesador) -> None:
        t = 0
        procesador.agregar_proceso(Proceso('a', t, 7), procesador.round_robin)
        procesador.agregar_proceso(Proceso('b', t, 6), procesador.round_robin)
        for i in range(0, 100):
            procesador.atender(i)

