# Test para verificar que el algoritmo SJF selecciona correctamente el proceso con menor tiempo de duración cuando ambos están disponibles desde el inicio.

from utils.file_loader import load_processes
from scheduling.sjf import sjf_scheduling

def test_sjf_order(tmp_path):
    file = tmp_path / "sjf.txt"
    # P1 y P2 llegan al mismo tiempo (t=0)
    # P2 tiene menor duración (2 vs 5)
    file.write_text("P1, 5, 0, 1\nP2, 2, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = sjf_scheduling(processes)
    # SJF debe ejecutar primero a P2
    assert gantt[0][2] == "P2"
