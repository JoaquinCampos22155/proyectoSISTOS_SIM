import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from utils.file_loader import load_processes
from scheduling.fifo import fifo_scheduling
from scheduling.sjf import sjf_scheduling
from gui.gantt_view import draw_gantt_chart

def iniciar_simulador_con_algoritmo(nombre_algoritmo, funcion_algoritmo, requiere_quantum=False):
    for widget in root.winfo_children():
        widget.destroy()

    # Obtener quantum si se requiere
    quantum = None
    if requiere_quantum:
        quantum = simpledialog.askinteger("Quantum", "Ingrese el quantum:", minvalue=1, maxvalue=100)
        if quantum is None:
            mostrar_submenu_algoritmos()
            return

    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if not archivo:
            return

        try:
            procesos = load_processes(archivo)

            if requiere_quantum:
                procesos_finales, gantt, avg_wt = funcion_algoritmo(procesos, quantum)
            else:
                procesos_finales, gantt, avg_wt = funcion_algoritmo(procesos)

            # Limpiar visualización previa
            for widget in root.winfo_children():
                if isinstance(widget, tk.Canvas) or isinstance(widget, tk.Label):
                    widget.destroy()

            draw_gantt_chart(root, gantt, procesos_finales, avg_wt)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la simulación:\n{e}")

    titulo = tk.Label(root, text=f"📊 Simulador - {nombre_algoritmo}", font=("Arial", 14, "bold"))
    titulo.pack(pady=10)

    btn_cargar = tk.Button(root, text="📂 Cargar archivo de procesos", font=("Arial", 12), command=seleccionar_archivo)
    btn_cargar.pack(pady=10)

    btn_volver = tk.Button(root, text="🔙 Volver a algoritmos", font=("Arial", 10), command=mostrar_submenu_algoritmos)
    btn_volver.pack(pady=10)

def mostrar_submenu_algoritmos():
    for widget in root.winfo_children():
        widget.destroy()

    titulo = tk.Label(root, text="🧠 Selecciona un algoritmo de calendarización", font=("Arial", 13, "bold"))
    titulo.pack(pady=15)

    tk.Button(root, text="📥 First In First Out (FIFO)", font=("Arial", 12),
              command=lambda: iniciar_simulador_con_algoritmo("FIFO", fifo_scheduling)).pack(pady=5)

    tk.Button(root, text="🧮 Shortest Job First (SJF)", font=("Arial", 12),
              command=lambda: iniciar_simulador_con_algoritmo("SJF", sjf_scheduling)).pack(pady=5)

    tk.Button(root, text="⏳ Shortest Remaining Time (SRT)", font=("Arial", 12),
              command=lambda: messagebox.showinfo("Pendiente", "SRT aún no implementado")).pack(pady=5)

    tk.Button(root, text="🌀 Round Robin", font=("Arial", 12),
              command=lambda: messagebox.showinfo("Pendiente", "Round Robin aún no implementado")).pack(pady=5)

    tk.Button(root, text="🔺 Priority Scheduling", font=("Arial", 12),
              command=lambda: messagebox.showinfo("Pendiente", "Priority aún no implementado")).pack(pady=5)

    tk.Button(root, text="🔙 Volver al menú principal", font=("Arial", 10),
              command=mostrar_menu_principal).pack(pady=15)

def iniciar_simulador_calendarizacion():
    mostrar_submenu_algoritmos()

def iniciar_simulador_sincronizacion():
    for widget in root.winfo_children():
        widget.destroy()

    placeholder = tk.Label(root, text="🔧 Simulador de sincronización aún no implementado", font=("Arial", 12), fg="gray")
    placeholder.pack(pady=40)

    boton_volver = tk.Button(root, text="🔙 Volver al menú principal", font=("Arial", 10), command=mostrar_menu_principal)
    boton_volver.pack(pady=10)

def mostrar_menu_principal():
    for widget in root.winfo_children():
        widget.destroy()

    titulo = tk.Label(root, text="🖥️ Simulador de Sistemas Operativos", font=("Arial", 14, "bold"))
    titulo.pack(pady=20)

    boton_calendarizacion = tk.Button(root, text="🧠 Simulador de Calendarización", font=("Arial", 12), command=iniciar_simulador_calendarizacion)
    boton_calendarizacion.pack(pady=10)

    boton_sincronizacion = tk.Button(root, text="🔒 Simulador de Sincronización", font=("Arial", 12), command=iniciar_simulador_sincronizacion)
    boton_sincronizacion.pack(pady=10)

    boton_salir = tk.Button(root, text="❌ Salir", font=("Arial", 12), command=root.quit)
    boton_salir.pack(pady=30)

# Crear ventana principal
root = tk.Tk()
root.title("Simulador de Sistemas Operativos")
root.geometry("600x500")

# Mostrar menú inicial
mostrar_menu_principal()

# Iniciar loop principal
root.mainloop()
