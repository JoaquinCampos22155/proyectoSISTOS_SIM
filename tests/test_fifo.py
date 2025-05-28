# test para verificar que el algoritmo FIFO (First In, First Out) ejecuta los procesos
# en el orden en que llegan, sin considerar duración ni prioridad.

from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
import pytest

def test_fifo_basic(tmp_path):
    file = tmp_path / "fifo.txt"
    # P1 llega en t=0, P2 en t=1
    file.write_text("P1, 3, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = fifo_scheduling(processes)
    # Validar que el promedio de espera sea un float
    assert isinstance(avg_wt, float)
    # El primer segmento del Gantt debe ser P1
    assert gantt[0][2] == "P1"
