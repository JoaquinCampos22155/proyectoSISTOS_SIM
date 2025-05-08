# scheduling/fifo.py

def fifo_scheduling(processes):
    """
    Ejecuta el algoritmo FIFO sobre una lista de procesos (ya leídos desde archivo)
    y retorna:
    - procesos ordenados con tiempos de espera y retorno calculados
    - una lista Gantt con tuplas (ciclo_inicio, ciclo_fin, pid)
    - el tiempo promedio de espera
    """
    # Ordenar por tiempo de llegada (AT)
    processes.sort(key=lambda p: p.at)

    current_time = 0
    gantt_chart = []

    for process in processes:
        # Si el proceso llega después del tiempo actual, se espera
        if current_time < process.at:
            current_time = process.at

        process.start_time = current_time
        process.completion_time = current_time + process.bt
        process.turnaround_time = process.completion_time - process.at
        process.waiting_time = process.start_time - process.at

        gantt_chart.append((process.start_time, process.completion_time, process.pid))

        current_time += process.bt

    # Calcular promedio de tiempos de espera
    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)

    return processes, gantt_chart, avg_waiting_time
