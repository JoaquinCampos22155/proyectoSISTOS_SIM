# Test para verificar que el algoritmo Round Robin con un quantum muy grande (>= mayor burst time)
# se comporta igual que FIFO, generando los mismos resultados en el diagrama de Gantt y tiempo de espera promedio.

import copy
import pytest
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from scheduling.round_robin import round_robin_scheduling

def test_rr_vs_fifo_equivalence(tmp_path):
    # P1, P2 y P3 con diferentes tiempos de llegada y duración
    content = """P1, 3, 0, 1
P2, 5, 1, 1
P3, 2, 2, 1
"""
    file = tmp_path / "proc.txt"
    file.write_text(content)
    processes = load_processes(str(file))
    # Round Robin con quantum grande debería comportarse como FIFO
    proc_fifo, gantt_fifo, avg_fifo = fifo_scheduling(copy.deepcopy(processes))
    proc_rr, gantt_rr, avg_rr = round_robin_scheduling(copy.deepcopy(processes), quantum=100)
    # Comparar diagramas de Gantt y promedios de espera
    assert gantt_fifo == gantt_rr
    assert pytest.approx(avg_fifo, rel=1e-3) == avg_rr

# Test para verificar que un quantum más pequeño en Round Robin genera mayor tiempo promedio de espera
# comparado con un quantum más grande, al haber más interrupciones de contexto.

def test_rr_quantum_effect(tmp_path):
    content = """P1, 4, 0, 1
P2, 4, 0, 1
"""
    file = tmp_path / "proc2.txt"
    file.write_text(content)
    processes = load_processes(str(file))
    # Comparar tiempo promedio de espera con quantum 1 y 4
    _, _, avg1 = round_robin_scheduling(copy.deepcopy(processes), quantum=1)
    _, _, avg4 = round_robin_scheduling(copy.deepcopy(processes), quantum=4)
    assert avg1 >= avg4
