# Test para verificar que el algoritmo SRT (Shortest Remaining Time) puede manejar correctamente
# una carga de procesos generados aleatoriamente sin lanzar errores, y produce una salida válida.

import pytest
import random
from utils.file_loader import load_processes
from scheduling.srt import srt_scheduling

def test_random_srt_no_errors(tmp_path):
    # Generar 10 procesos aleatorios con burst time entre 1-10 y arrival time entre 0-5
    lines = []
    for i in range(10):
        pid = f"P{i}"
        bt = random.randint(1, 10)
        at = random.randint(0, 5)
        lines.append(f"{pid}, {bt}, {at}, 1")
    content = "\n".join(lines)
    file = tmp_path / "rand.txt"
    file.write_text(content)
    processes = load_processes(str(file))
    
    # Ejecutar el algoritmo SRT y validar la salida
    proc_final, gantt, avg_wt = srt_scheduling(processes)
    assert isinstance(gantt, list)
    assert all(isinstance(interval, tuple) for interval in gantt)
    assert avg_wt >= 0
