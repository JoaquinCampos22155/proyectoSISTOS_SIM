# Test para verificar que al usar copy.deepcopy, la copia de los procesos permanece sin modificar
# después de ejecutar un algoritmo de planificación (en este caso FIFO), asegurando independencia de objetos.

import copy
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling

def test_deepcopy_independence(tmp_path):
    file = tmp_path / "dep.txt"
    # Dos procesos con llegada en t=0 y t=1
    file.write_text("P1, 3, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_copy = copy.deepcopy(processes)
    fifo_scheduling(processes)
    # Verificar que la copia no se haya modificado (remaining_time debe ser igual a burst time)
    assert proc_copy[0].remaining_time == proc_copy[0].bt
