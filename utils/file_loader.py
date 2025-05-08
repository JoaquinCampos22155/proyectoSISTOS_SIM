from scheduling.process import Process

def load_processes(file_path):
    processes = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                pid, bt, at, priority = line.strip().split(",")
                processes.append(Process(pid.strip(), int(bt), int(at), int(priority)))
    return processes
