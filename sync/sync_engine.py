from sync.state import State

def run_sync_simulation(procesos, recursos, acciones, modo="mutex"):
    max_ciclo = max(a.cycle for a in acciones) + 20
    acciones_por_ciclo = {ciclo: [] for ciclo in range(max_ciclo)}
    for acc in acciones:
        acciones_por_ciclo[acc.cycle].append(acc)

    gantt = []
    waiting_queues = {r: [] for r in recursos}
    resource_holders = {r: [] for r in recursos}

    for ciclo in range(max_ciclo):
        # 1. Liberar recursos (se usan solo 1 ciclo)
        for r_name, holders in resource_holders.items():
            if holders:
                recursos[r_name].available += len(holders)
                resource_holders[r_name] = []

        # 2. Reintentos primero (procesos en espera tienen prioridad)
        for r_name in recursos:
            recurso = recursos[r_name]
            queue = waiting_queues[r_name]
            nuevos_intentos = []

            if modo == "mutex":
                if not resource_holders[r_name] and queue:
                    acc = queue.pop(0)
                    resource_holders[r_name].append(acc.pid)
                    gantt.append((ciclo, acc.pid, r_name, State.ACCESSED))
                # Los que no alcanzaron quedan para después
                nuevos_intentos += queue

            elif modo == "semaforo":
                for acc in queue:
                    if recurso.available > 0:
                        recurso.available -= 1
                        resource_holders[r_name].append(acc.pid)
                        gantt.append((ciclo, acc.pid, r_name, State.ACCESSED))
                    else:
                        nuevos_intentos.append(acc)

            waiting_queues[r_name] = nuevos_intentos

        # 3. Luego se procesan las acciones nuevas del ciclo actual
        for acc in acciones_por_ciclo.get(ciclo, []):
            recurso = recursos[acc.resource_name]
            r_name = acc.resource_name

            if modo == "mutex":
                if not resource_holders[r_name]:  # Recurso libre
                    resource_holders[r_name].append(acc.pid)
                    gantt.append((ciclo, acc.pid, r_name, State.ACCESSED))
                else:
                    waiting_queues[r_name].append(acc)
                    gantt.append((ciclo, acc.pid, r_name, State.WAITING))

            elif modo == "semaforo":
                if recurso.available > 0:
                    recurso.available -= 1
                    resource_holders[r_name].append(acc.pid)
                    gantt.append((ciclo, acc.pid, r_name, State.ACCESSED))
                else:
                    waiting_queues[r_name].append(acc)
                    gantt.append((ciclo, acc.pid, r_name, State.WAITING))

    return gantt
