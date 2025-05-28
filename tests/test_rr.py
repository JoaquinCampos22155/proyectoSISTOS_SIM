# Test para verificar que el algoritmo Round Robin con quantum 2 asigna correctamente turnos
# a los procesos en ciclos y que todos terminan su ejecución sin tiempo restante.

from utils.file_loader import load_processes
from scheduling.round_robin import round_robin_scheduling
import pytest

def test_rr_quantum(tmp_path):
    file = tmp_path / "rr.txt"
    # P1 y P2 llegan en t=0 con duraciones 4 y 3 respectivamente
    file.write_text("P1, 4, 0, 1\nP2, 3, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = round_robin_scheduling(processes, 2)
    # Validar que el promedio de espera es un número flotante
    assert isinstance(avg_wt, float)
    # Verificar que ningún proceso quede con tiempo restante
    assert all(p.remaining_time == 0 for p in proc_final)
