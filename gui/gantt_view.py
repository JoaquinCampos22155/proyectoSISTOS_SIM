import tkinter as tk
from random import randint

# Mapa de colores únicos por proceso
def get_color_map(processes):
    color_map = {}
    for p in processes:
        if p.pid not in color_map:
            color_map[p.pid] = f'#{randint(100,255):02x}{randint(100,255):02x}{randint(100,255):02x}'
    return color_map

def draw_gantt_chart(root, gantt_chart, procesos, avg_wt, compacto=False):
    # Parámetros compactos si aplica
    if compacto:
        canvas_height = 90
        block_height = 25
        block_y = 25
        block_width = 20
        font_pid = ("Arial", 7)
        font_ciclo = ("Arial", 6)
        font_avg = ("Arial", 9)
    else:
        canvas_height = 150
        block_height = 50
        block_y = 40
        block_width = 40
        font_pid = ("Arial", 9)
        font_ciclo = ("Arial", 8)
        font_avg = ("Arial", 10, "bold")

    canvas = tk.Canvas(root, height=canvas_height, width=800, bg="white", scrollregion=(0, 0, 10000, canvas_height))
    h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.config(xscrollcommand=h_scroll.set)

    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Mostrar métricas
    avg_label = tk.Label(root, text=f"Tiempo promedio de espera: {avg_wt:.2f} ciclos", font=font_avg)
    avg_label.pack(side=tk.BOTTOM, pady=5)

    color_map = get_color_map(procesos)

    # Lista para ciclos simulados
    timeline = []
    for start, end, pid in gantt_chart:
        for t in range(start, end):
            timeline.append((t, pid))

    def animate(index=0):
        if index >= len(timeline): return

        ciclo, pid = timeline[index]
        x0 = ciclo * block_width
        x1 = x0 + block_width
        color = color_map[pid]

        canvas.create_rectangle(x0, block_y, x1, block_y + block_height, fill=color, outline='black')
        canvas.create_text((x0 + x1)//2, block_y + block_height//2, text=pid, fill="black", font=font_pid)
        canvas.create_text(x0, block_y + block_height + 5, text=str(ciclo), anchor="n", font=font_ciclo)

        root.after(200, animate, index + 1)  # Velocidad: 200ms por ciclo

    animate()
