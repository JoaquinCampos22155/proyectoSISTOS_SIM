import copy
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling

def test_deepcopy_independence(tmp_path):
    file = tmp_path / "dep.txt"
    file.write_text("P1, 3, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_copy = copy.deepcopy(processes)
    fifo_scheduling(processes)
    # original list mutated? copy should remain original remaining_time
    assert proc_copy[0].remaining_time == proc_copy[0].bt