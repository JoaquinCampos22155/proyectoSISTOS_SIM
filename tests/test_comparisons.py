import copy
import pytest
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from scheduling.round_robin import round_robin_scheduling

def test_rr_vs_fifo_equivalence(tmp_path):
    # When quantum >= max burst, RR should behave like FIFO
    content = """P1, 3, 0, 1
P2, 5, 1, 1
P3, 2, 2, 1
"""
    file = tmp_path / "proc.txt"
    file.write_text(content)
    processes = load_processes(str(file))
    # Use a large quantum
    proc_fifo, gantt_fifo, avg_fifo = fifo_scheduling(copy.deepcopy(processes))
    proc_rr, gantt_rr, avg_rr = round_robin_scheduling(copy.deepcopy(processes), quantum=100)
    # Gantt charts should match in segments and order
    assert gantt_fifo == gantt_rr
    assert pytest.approx(avg_fifo, rel=1e-3) == avg_rr

def test_rr_quantum_effect(tmp_path):
    content = """P1, 4, 0, 1
P2, 4, 0, 1
"""
    file = tmp_path / "proc2.txt"
    file.write_text(content)
    processes = load_processes(str(file))
    # Smaller quantum should not improve average waiting
    _, _, avg1 = round_robin_scheduling(copy.deepcopy(processes), quantum=1)
    _, _, avg4 = round_robin_scheduling(copy.deepcopy(processes), quantum=4)
    assert avg1 >= avg4