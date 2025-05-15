from utils.file_loader import load_processes
import pytest

def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")
    processes = load_processes(str(file))
    assert processes == []