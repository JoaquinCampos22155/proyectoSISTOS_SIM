from utils.file_loader import load_processes
from scheduling.round_robin import round_robin_scheduling
import pytest

def test_rr_quantum(tmp_path):
    file = tmp_path / "rr.txt"
    file.write_text("P1, 4, 0, 1\nP2, 3, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = round_robin_scheduling(processes, 2)
    assert isinstance(avg_wt, float)
    # Ensure no process has remaining_time > 0
    assert all(p.remaining_time == 0 for p in proc_final)

def test_rr_invalid_quantum(tmp_path):
    file = tmp_path / "rr2.txt"
    file.write_text("P1, 3, 0, 1\n")
    processes = load_processes(str(file))
    with pytest.raises(Exception):
        round_robin_scheduling(processes, 0)