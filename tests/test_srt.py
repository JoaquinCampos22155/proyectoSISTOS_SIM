from utils.file_loader import load_processes
from scheduling.srt import srt_scheduling

def test_srt_preemptive(tmp_path):
    file = tmp_path / "srt.txt"
    # P1 starts, then P2 arrives with shorter time
    file.write_text("P1, 5, 0, 1\nP2, 2, 1, 1\n")
    processes = load_processes(str(file))
    proc_final, gantt, avg_wt = srt_scheduling(processes)
    # At time=1, P2 should preempt P1
    # So second segment pid is P2
    assert gantt[1][2] == "P2"