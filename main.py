# main.py

from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from gui.gantt_view import draw_gantt_chart
import tkinter as tk

def main():
    ruta = "data/procesos.txt"  # Reemplaza con tu ruta real
    procesos = load_processes(ruta)
    
    print("Procesos cargados:")
    for p in procesos:
        print(p)

    procesos_finales, gantt, avg_wt = fifo_scheduling(procesos)

    print("\nResultados FIFO:")
    for p in procesos_finales:
        print(f"{p.pid}: Waiting={p.waiting_time}, Turnaround={p.turnaround_time}")

    print("\nGantt Chart:")
    for inicio, fin, pid in gantt:
        print(f"[{inicio}-{fin}] {pid}", end=" | ")

    print(f"\n\nTiempo promedio de espera: {avg_wt:.2f} ciclos")

    # Visualización gráfica
    root = tk.Tk()
    root.title("Simulación de FIFO - Gantt Dinámico")
    draw_gantt_chart(root, gantt, procesos_finales, avg_wt)  # <- se pasa avg_wt también
    root.mainloop()

if __name__ == "__main__":
    main()
