from utils.file_loader import load_processes
from scheduling.sjf import sjf_scheduling

def test_sjf_order(tmp_path):
    file = tmp_path / "sjf.txt"
    file.write_text("P1, 5, 0, 1\nP2, 2, 0, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = sjf_scheduling(processes)
    # SJF should run P2 first
    assert gantt[0][2] == "P2"