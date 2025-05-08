from collections import deque

def round_robin_scheduling(processes, quantum):
    """
    Algoritmo Round Robin con quantum configurable.
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
    cola = deque()
    timeline = []

    procesos = sorted(processes, key=lambda p: p.at)  # ordenar por arrival time
    arrival_index = 0  # para ingresar nuevos procesos

    while completed < n:
        # Agregar procesos que han llegado
        while arrival_index < n and processes[arrival_index].at <= time:
            cola.append(processes[arrival_index])
            arrival_index += 1

        if cola:
            current = cola.popleft()

            exec_time = min(current.remaining_time, quantum)

            for _ in range(exec_time):
                timeline.append((time, current.pid))
                time += 1

                # Ingresar procesos que llegaron durante este tiempo
                while arrival_index < n and processes[arrival_index].at <= time:
                    cola.append(processes[arrival_index])
                    arrival_index += 1

            current.remaining_time -= exec_time

            if current.remaining_time == 0:
                current.completion_time = time
                current.turnaround_time = current.completion_time - current.at
                current.waiting_time = current.turnaround_time - current.bt
                procesos_terminados.append(current)
                completed += 1
            else:
                cola.append(current)  # vuelve al final de la cola
        else:
            timeline.append((time, None))  # CPU ocioso
            time += 1

    # Convertimos timeline a bloques Gantt [(inicio, fin, PID)]
    if timeline:
        start = timeline[0][0]
        last_pid = timeline[0][1]

        for i in range(1, len(timeline)):
            pid = timeline[i][1]
            if pid != last_pid:
                gantt_chart.append((start, timeline[i][0], last_pid))
                start = timeline[i][0]
                last_pid = pid

        gantt_chart.append((start, timeline[-1][0] + 1, last_pid))

    avg_waiting_time = sum(p.waiting_time for p in procesos_terminados) / n
    return procesos_terminados, gantt_chart, avg_waiting_time
