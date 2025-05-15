from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
import pytest

def test_fifo_basic(tmp_path):
    file = tmp_path / "fifo.txt"
    file.write_text("P1, 3, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = fifo_scheduling(processes)
    assert isinstance(avg_wt, float)
    # First segment must start with P1 at time 0
    assert gantt[0][2] == "P1"