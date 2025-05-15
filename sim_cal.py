import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from utils.file_loader import load_processes
from gui.gantt_view import draw_gantt_chart

def iniciar_simulador_con_algoritmo(root, nombre_algoritmo, funcion_algoritmo, requiere_quantum, volver_callback):
    for widget in root.winfo_children():
        widget.destroy()

    archivo_procesos = tk.StringVar()
    quantum = None

    # === Marco izquierdo con subdivisión ===
    frame_izq = tk.Frame(root)
    frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_menu = tk.Frame(frame_izq)
    frame_menu.pack(side=tk.TOP, fill=tk.X)

    frame_vista = tk.Frame(frame_izq)
    frame_vista.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # === Marco derecho ===
    frame_der = tk.Frame(root, width=300, bg="#f0f0f0")
    frame_der.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(frame_der, text="📄 Archivo cargado", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=5)
    label_nombre_archivo = tk.Label(frame_der, text="(ninguno)", font=("Arial", 10), bg="#f0f0f0", wraplength=280)
    label_nombre_archivo.pack(padx=10)

    vista_archivo = tk.Text(frame_der, height=30, width=40, bg="#f7f7f7", font=("Courier", 9))
    vista_archivo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    vista_archivo.config(state=tk.DISABLED)

    def mostrar_contenido_archivo(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            contenido = f"Error al leer el archivo:\n{e}"
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.insert(tk.END, contenido)
        vista_archivo.config(state=tk.DISABLED)

    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(title="Seleccionar archivo de procesos", filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return
        archivo_procesos.set(archivo)
        label_nombre_archivo.config(text=archivo.split("/")[-1])
        mostrar_contenido_archivo(archivo)
        if not requiere_quantum or (requiere_quantum and quantum is not None):
            ejecutar_simulacion()

    def ejecutar_simulacion():
        try:
            procesos = load_processes(archivo_procesos.get())
            resultado = funcion_algoritmo(procesos, quantum) if requiere_quantum else funcion_algoritmo(procesos)
            procesos_finales, gantt, avg_wt = resultado

            for widget in frame_vista.winfo_children():
                widget.destroy()

            draw_gantt_chart(frame_vista, gantt, procesos_finales, avg_wt)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la simulación:\n{e}")

    def reset_simulacion():
        confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas resetear la simulación?")
        if not confirmacion:
            return
        archivo_procesos.set("")
        label_nombre_archivo.config(text="(ninguno)")
        vista_archivo.config(state=tk.NORMAL)
        vista_archivo.delete(1.0, tk.END)
        vista_archivo.config(state=tk.DISABLED)
        for widget in frame_vista.winfo_children():
            widget.destroy()

    def rerun_simulacion():
        for widget in frame_vista.winfo_children():
            widget.destroy()
        ejecutar_simulacion()

    if requiere_quantum:
        quantum = simpledialog.askinteger("Quantum", "Ingrese el quantum:", minvalue=1, maxvalue=100)
        if quantum is None:
            volver_callback()
            return

    # === Botones del panel izquierdo ===
    tk.Label(frame_menu, text=f"📊 Simulador - {nombre_algoritmo}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(frame_menu, text="📂 Cargar archivo de procesos", font=("Arial", 12), command=seleccionar_archivo).pack(pady=10)
    tk.Button(frame_menu, text="▶ Ejecutar de nuevo", font=("Arial", 11), command=ejecutar_simulacion).pack(pady=5)
    tk.Button(frame_menu, text="🔁 RERUN", bg="#ccf5ff", width=20, command=rerun_simulacion).pack(pady=2)
    tk.Button(frame_menu, text="⚠️ RESET", bg="#ffdddd", width=20, command=reset_simulacion).pack(pady=2)
    tk.Button(frame_menu, text="🔙 Volver a algoritmos", font=("Arial", 10), command=volver_callback).pack(pady=20)
