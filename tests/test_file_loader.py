import pytest
from utils.file_loader import load_processes

def test_load_processes_valid(tmp_path):
    file = tmp_path / "proc.txt"
    file.write_text("P1, 4, 0, 1\nP2, 3, 1, 2\n")
    processes = load_processes(str(file))
    assert len(processes) == 2
    assert processes[0].pid == "P1"
    assert processes[1].at == 1

def test_load_processes_invalid(tmp_path):
    file = tmp_path / "bad.txt"
    file.write_text("P1, 4, 0\n")  # missing priority
    with pytest.raises(Exception):
        load_processes(str(file))