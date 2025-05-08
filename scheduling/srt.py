# scheduling/srt.py

def srt_scheduling(processes):
    """
    Algoritmo SRT (Shortest Remaining Time), expropiativo.
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

    timeline = []  # nuevo: lista (tiempo, pid)

    while completed < n:
        ready = [p for p in processes if p.at <= time and p not in procesos_terminados and p.remaining_time > 0]

        if ready:
            ready.sort(key=lambda p: (p.remaining_time, p.at))
            current = ready[0]

            timeline.append((time, current.pid))  # agregamos ciclo actual

            current.remaining_time -= 1

            if current.remaining_time == 0:
                current.completion_time = time + 1
                current.turnaround_time = current.completion_time - current.at
                current.waiting_time = current.turnaround_time - current.bt
                procesos_terminados.append(current)
                completed += 1
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
