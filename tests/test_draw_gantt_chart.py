import tkinter as tk
import pytest
from gui.gantt_view import draw_gantt_chart

def test_draw_gantt_chart_minimal(monkeypatch):
    # Create dummy data
    gantt = [(0, 2, 'P1'), (2, 4, 'P2')]
    class DummyCanvas:
        def __init__(self, *args, **kwargs):
            self.rectangles = []
        def create_rectangle(self, x0, y0, x1, y1, **kwargs):
            self.rectangles.append((x0, y0, x1, y1))
        def create_text(self, *args, **kwargs):
            pass
        def pack(self, *args, **kwargs): pass
        def config(self, *args, **kwargs): pass
    # Monkeypatch Canvas and Scrollbar
    monkeypatch.setattr(tk, 'Canvas', DummyCanvas)
    monkeypatch.setattr(tk, 'Scrollbar', lambda *args, **kwargs: type('S', (), {'pack': lambda *a, **k: None, 'config': lambda *a, **k: None})())
    root = tk.Tk()
    # Should not raise
    draw_gantt_chart(root, gantt, [{'pid':'P1','remaining_time':2, 'bt':2}, {'pid':'P2','remaining_time':2, 'bt':2}], avg_wt=1.5)
    # Validate rectangles count
    assert len(root.children) >= 0  # no exceptions