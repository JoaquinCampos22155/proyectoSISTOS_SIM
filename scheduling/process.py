class Process:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = bt  # Burst Time
        self.at = at  # Arrival Time
        self.priority = priority
        self.remaining_time = bt  # Solo útil para SRT y RR
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return f"Process({self.pid}, BT={self.bt}, AT={self.at}, Prio={self.priority})"
