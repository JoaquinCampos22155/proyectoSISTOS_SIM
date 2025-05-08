# scheduling/sjf.py

def sjf_scheduling(processes):
    """
    Algoritmo SJF no expropiativo.
    Retorna:
    - Lista de procesos con tiempos calculados
    - Lista Gantt [(inicio, fin, PID)]
    - Tiempo promedio de espera
    """
    n = len(processes)
    time = 0
    completed = 0
    gantt_chart = []
    ready_queue = []
    procesos_terminados = []

    # Bandera para saber si ya se ejecutó
    while completed < n:
        # Agregar a ready queue todos los procesos que han llegado
        for p in processes:
            if p.at <= time and p not in ready_queue and p not in procesos_terminados:
                ready_queue.append(p)

        if ready_queue:
            # Seleccionar el proceso con menor Burst Time
            ready_queue.sort(key=lambda p: (p.bt, p.at))  # Si empatan en BT, el de menor AT

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
            time += 1  # Espera si ningún proceso ha llegado

    avg_waiting_time = sum(p.waiting_time for p in procesos_terminados) / n
    return procesos_terminados, gantt_chart, avg_waiting_time
