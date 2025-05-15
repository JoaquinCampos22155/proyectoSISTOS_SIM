import pytest
from utils.sync_loader import load_processes_sync, load_resources, load_actions
from sync.sync_engine import run_sync_simulation

def test_sync_engine_basic(tmp_path):
    # Prepare simple sync files
    proc_file = tmp_path / "proc.txt"
    proc_file.write_text("P1, 1, 0\n")
    res_file = tmp_path / "res.txt"
    res_file.write_text("R1, 1\n")
    acts_file = tmp_path / "acts.txt"
    acts_file.write_text("P1, READ, R1, 0\n")
    processes = load_processes_sync(str(proc_file))
    resources = load_resources(str(res_file))
    actions = load_actions(str(acts_file))
    # Should not raise and return a timeline list
    gantt = run_sync_simulation(processes, resources, actions, modo="mutex")
    assert isinstance(gantt, list)
    # Timeline entries should have at least one tuple/list
    assert len(gantt) > 0
    assert hasattr(gantt[0], '__iter__')