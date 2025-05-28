# Test para verificar que el algoritmo de planificación por prioridades selecciona correctamente
# el proceso con mayor prioridad (valor numérico menor) cuando varios procesos llegan al mismo tiempo.

from utils.file_loader import load_processes
from scheduling.priority import priority_scheduling

def test_priority_basic(tmp_path):
    file = tmp_path / "pr.txt"
    # P1 y P2 llegan en t=0, pero P2 tiene mayor prioridad (1 < 2)
    file.write_text("P1, 3, 0, 2\nP2, 3, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = priority_scheduling(processes)
    # P2 debe ejecutarse primero
    assert gantt[0][2] == "P2"
