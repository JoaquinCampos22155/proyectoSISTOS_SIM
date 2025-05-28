# Test para verificar que el algoritmo SRT (Shortest Remaining Time) realiza la expulsión preemptive correctamente
# cuando un nuevo proceso llega con menor tiempo restante que el actual en ejecución.

from utils.file_loader import load_processes
from scheduling.srt import srt_scheduling

def test_srt_preemptive(tmp_path):
    file = tmp_path / "srt.txt"
    # P1 empieza en t=0 con duración 5
    # P2 llega en t=1 con duración 2 (menor que el tiempo restante de P1)
    file.write_text("P1, 5, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = srt_scheduling(processes)
    # En t=1, P2 debe expulsar a P1
    # Por lo tanto, el segundo segmento (índice 1) debe ser de P2
    assert gantt[1][2] == "P2"
