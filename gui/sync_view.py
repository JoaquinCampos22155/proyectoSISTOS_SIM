import tkinter as tk
from sync.state import State
from random import randint

def draw_sync_timeline(root, gantt_sync, velocidad=100):
    """
    Visualiza la sincronización como un timeline animado, ciclo a ciclo.
    Eje X = ciclos, eje Y = procesos.
    """
    # Obtener procesos únicos ordenados
    procesos_unicos = sorted(list({pid for _, pid, _, _ in gantt_sync}))
    proceso_fila = {pid: idx for idx, pid in enumerate(procesos_unicos)}

    block_width = 40
    block_height = 40
    margen_izquierdo = 100
    margen_superior = 40

    total_ciclos = max(c for c, _, _, _ in gantt_sync) + 1
    total_procesos = len(proceso_fila)

    canvas = tk.Canvas(
        root,
        width=800,
        height=400,
        bg="white",
        scrollregion=(0, 0, margen_izquierdo + total_ciclos * block_width, margen_superior + total_procesos * block_height + 100)
    )
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.config(xscrollcommand=h_scroll.set)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    v_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    canvas.config(yscrollcommand=v_scroll.set)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Colores únicos por proceso
    color_map = {}
    def get_color(pid, state):
        if state == State.WAITING:
            return "#ff6347"  # rojo tomate
        if pid not in color_map:
            color_map[pid] = f'#{randint(100,255):02x}{randint(100,255):02x}{randint(100,255):02x}'
        return color_map[pid]

    # Etiquetas verticales de procesos
    for pid, idx in proceso_fila.items():
        y = margen_superior + idx * block_height + block_height // 2
        canvas.create_text(margen_izquierdo - 10, y, text=pid, anchor="e", font=("Arial", 10, "bold"))

    # Ordenar por ciclo para animación secuencial
    timeline = sorted(gantt_sync, key=lambda x: x[0])

    def animate(index=0):
        if index >= len(timeline):
            return

        ciclo, pid, recurso, state = timeline[index]
        fila = proceso_fila[pid]

        x0 = margen_izquierdo + ciclo * block_width
        y0 = margen_superior + fila * block_height
        x1 = x0 + block_width
        y1 = y0 + block_height

        color = get_color(pid, state)
        text_color = "white" if state == State.WAITING else "black"

        # Rectángulo para el uso o espera del recurso
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

        # Recurso en el centro
        canvas.create_text((x0 + x1)//2, (y0 + y1)//2 - 5, text=recurso, font=("Arial", 8), fill=text_color)

        # Ciclo abajo
        canvas.create_text((x0 + x1)//2, y1 - 10, text=str(ciclo), font=("Arial", 7), fill="gray")

        # Siguiente acción
        root.after(velocidad, animate, index + 1)

    # Opcional: Agregar leyenda
    canvas.create_text(10, 10, anchor="nw", text=" 🟥 WAITING color rojo", font=("Arial", 10, "italic"))

    animate()
