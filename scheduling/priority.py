def priority_scheduling(processes):
    """
    Algoritmo de Priority Scheduling no expropiativo.
    Devuelve:
    - Lista de procesos con tiempos calculados
    - Lista Gantt [(inicio, fin, PID)]
    - Tiempo promedio de espera
    """
    n = len(processes)
    time = 0
    completed = 0
    gantt_chart = []
    procesos_terminados = []
    ready_queue = []

    while completed < n:
        # Procesos que han llegado y no han sido ejecutados
        for p in processes:
            if p.at <= time and p not in procesos_terminados and p not in ready_queue:
                ready_queue.append(p)

        if ready_queue:
            # Elegir el de mayor prioridad (menor valor numérico)
            ready_queue.sort(key=lambda p: (p.priority, p.at))
            current = ready_queue.pop(0)

            current.start_time = time
            current.completion_time = time + current.bt
            current.turnaround_time = current.completion_time - current.at
            current.waiting_time = current.start_time - current.at

            gantt_chart.append((current.start_time, current.completion_time, current.pid))
            procesos_terminados.append(current)

            time += current.bt
            completed += 1
        else:
            time += 1  # CPU ocioso

    avg_waiting_time = sum(p.waiting_time for p in procesos_terminados) / n
    return procesos_terminados, gantt_chart, avg_waiting_time
