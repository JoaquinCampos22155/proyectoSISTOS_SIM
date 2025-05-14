from scheduling.process import Process
from sync.resource import Resource
from sync.action import Action

def load_processes_sync(path):
    procesos = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                pid, bt, at, prio = line.strip().split(',')
                procesos.append(Process(pid.strip(), int(bt), int(at), int(prio)))
    return procesos

def load_resources(path):
    recursos = {}
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                name, count = line.strip().split(',')
                recursos[name.strip()] = Resource(name.strip(), int(count))
    return recursos

def load_actions(path):
    acciones = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                pid, tipo, recurso, ciclo = line.strip().split(',')
                acciones.append(Action(pid.strip(), tipo.strip(), recurso.strip(), ciclo.strip()))
    return acciones
