# Tests para validar la función load_processes:

import pytest
from utils.file_loader import load_processes
# se asegura que una entrada válida se cargue correctamente en objetos de proceso.

def test_load_processes_valid(tmp_path):
    file = tmp_path / "proc.txt"
    # Dos procesos con todos los campos: PID, burst time, arrival time y prioridad
    file.write_text("P1, 4, 0, 1\nP2, 3, 1, 2\n")
    processes = load_processes(str(file))
    assert len(processes) == 2
    assert processes[0].pid == "P1"
    assert processes[1].at == 1

# se verifica que una entrada inválida y q genere una excepción apropiada.
def test_load_processes_invalid(tmp_path):
    file = tmp_path / "bad.txt"
    # Entrada con un campo faltante (sin prioridad)
    file.write_text("P1, 4, 0\n")
    with pytest.raises(Exception):
        load_processes(str(file))
