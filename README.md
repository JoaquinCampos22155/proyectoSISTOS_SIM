# proyectoSISTOS_SIM
### Simulador visual de algoritmos de **calendarización** y mecanismos de **sincronización** para Sistemas Operativos

---

## Algoritmos de Calendarización Implementados

- **FIFO** – First In First Out
- **SJF** – Shortest Job First
- **SRT** – Shortest Remaining Time (expropiativo)
- **Round Robin** – con *quantum* configurable
- **Priority** – por prioridad de ejecución

### Formato del archivo `procesosCal.txt`

| Columna   | Descripción               |
|-----------|---------------------------|
| PID       | Identificador del proceso |
| BT        | Burst Time (tiempo CPU)   |
| AT        | Arrival Time              |
| Priority  | Nivel de prioridad        |


`Ejemplo: P1, 8, 0, 1`

---

## 🔒 Mecanismos de Sincronización Soportados

- **Mutex Lock**
- **Semáforos**

### Formato del archivo `procesosMec.txt`

| Columna   | Descripción               |
|-----------|---------------------------|
| PID       | Identificador del proceso |
| BT        | Burst Time (tiempo CPU)   |
| AT        | Arrival Time              |
| Priority  | Nivel de prioridad        |

`Ejemplo: P1, 8, 0, 1`


¿Qué significa cada columna en el ______.txt dentro de la sincronización?

NOMBRE RECURSO: Nombre del recurso 

CONTADOR: Contador

`Ejemplo: R1, 1`

¿Qué significa cada columna en el ______.txt dentro de la sincronización?

PID: identificador del proceso

ACCION: Burst Time 

RECURSO: Arrival Time 

CICLO: prioridad

`Ejemplo: P1, READ, R1, 0`

---

## Comparación de Algoritmos

Este simulador permite **comparar visualmente dos algoritmos de calendarización** ejecutando ambos con el mismo conjunto de procesos. Los resultados son desplegados de forma paralela para comparar su comportamiento y eficiencia.

Al comparar:
- Se solicitan los algoritmos a comparar.
- Si uno de ellos es **Round Robin**, se solicita el *quantum* antes de la simulación.
- Ambos algoritmos usan una **misma copia de los procesos** para asegurar equidad.
- Se puede hacer **reset global** o **rerun global** desde la interfaz para re-ejecutar las simulaciones con los mismos parámetros.

**Nota:** Round Robin puede arrojar errores si todos los procesos llegan al mismo tiempo (`Arrival Time = 1`), ya que su cola dinámica depende del orden de llegada.

---

## 🚀 ¿Cómo ejecutar el simulador?

1. Asegúrate de tener Python 3.7+ instalado.

2. Ejecuta el archivo principal:

```bash
python main_gui.py
