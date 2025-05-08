# main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from gui.gantt_view import draw_gantt_chart

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de procesos",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if not archivo:
        return

    try:
        procesos = load_processes(archivo)
        procesos_finales, gantt, avg_wt = fifo_scheduling(procesos)

        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas) or isinstance(widget, tk.Label):
                widget.destroy()

        draw_gantt_chart(root, gantt, procesos_finales, avg_wt)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

# Crear ventana
root = tk.Tk()
root.title("Simulador FIFO - Selector de archivo")

# Botón principal
boton_cargar = tk.Button(root, text="📂 Cargar archivo de procesos", font=("Arial", 12), command=seleccionar_archivo)
boton_cargar.pack(pady=20)

root.mainloop()
