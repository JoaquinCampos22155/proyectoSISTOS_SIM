# Test para verificar que la función load_processes devuelve una lista vacía
# cuando se proporciona un archivo de entrada vacío.

from utils.file_loader import load_processes
import pytest

def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")
    processes = load_processes(str(file))
    assert processes == []
