from utils.file_loader import load_processes
from scheduling.priority import priority_scheduling

def test_priority_basic(tmp_path):
    file = tmp_path / "pr.txt"
    file.write_text("P1, 3, 0, 2\nP2, 3, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = priority_scheduling(processes)
    # P2 has higher priority (1 < 2) so runs first
    assert gantt[0][2] == "P2"